"""Суррогатная модель уравнения состояния алюминия (PINN) — обёртка для инференса.

Пример:
    >>> from eos_surrogate import EOSSurrogate
    >>> eos = EOSSurrogate("pinn_best_physics.pt", "normalization.json")
    >>> P, e = eos.predict(rho=2.7, T=1e4)
    >>> cs = eos.sound_speed(rho=2.7, T=1e4)
    >>> flags = eos.check_physics(rho=2.7, T=1e4)
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn

C_CGS = 2.99792458e10   # скорость света, см/с
GPA_TO_CGS = 1e10       # ГПа/(г/см^3) -> см^2/с^2
KJ_TO_CGS = 1e10        # кДж/(г*К)   -> см^2/(с^2*К)


class _Net(nn.Module):
    """Полносвязная сеть 2 -> width -> width -> width/2 -> 2 (tanh)."""

    def __init__(self, width: int = 128):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(2, width), nn.Tanh(),
            nn.Linear(width, width), nn.Tanh(),
            nn.Linear(width, width // 2), nn.Tanh(),
            nn.Linear(width // 2, 2))

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.net(x)


class EOSSurrogate:
    """Термодинамически согласованный суррогат EOS: P(ρ,T), e(ρ,T), c_s(ρ,T).

    Модель работает в логарифмических координатах: входы log10(ρ), log10(T)
    нормируются в [0, 1], давление предсказывается как log10(P), энергия — как e.
    Производные для скорости звука считаются через autograd.

    Attributes:
        norm: словарь параметров нормализации из normalization.json.
        width: ширина скрытого слоя модели.
    """

    def __init__(self, weights: str | Path = "pinn_best_physics.pt",
                 norm_path: str | Path = "normalization.json",
                 width: int = 128):
        """Загружает веса и параметры нормализации.

        Args:
            weights: путь к state_dict модели (.pt).
            norm_path: путь к normalization.json.
            width: ширина скрытого слоя; должна совпадать с обученной моделью.

        Raises:
            FileNotFoundError: если файл весов или нормализации отсутствует.
        """
        self.norm = json.loads(Path(norm_path).read_text())
        self.width = width
        self.model = _Net(width)
        self.model.load_state_dict(torch.load(weights, map_location="cpu"))
        self.model.eval()
        n = self.norm["inputs"]
        o = self.norm["outputs"]
        self._lr = (n["log_rho"]["min"], n["log_rho"]["max"])
        self._lt = (n["log_T"]["min"], n["log_T"]["max"])
        self._P = (o["P"]["min"], o["P"]["max"])
        self._e = (o["e"]["min"], o["e"]["max"])
        self._lp = (np.log10(self._P[0]), np.log10(self._P[1]))

    # ------------------------------------------------------------------ utils
    def _encode(self, rho, T):
        rho = np.asarray(rho, dtype=np.float64)
        T = np.asarray(T, dtype=np.float64)
        if np.any(rho <= 0) or np.any(T <= 0):
            raise ValueError("rho и T должны быть положительными")
        lr = np.log10(rho)
        lt = np.log10(T)
        x = np.stack([(lr - self._lr[0]) / (self._lr[1] - self._lr[0]),
                      (lt - self._lt[0]) / (self._lt[1] - self._lt[0])], -1)
        inside = ((x >= -0.02) & (x <= 1.02)).all(-1)
        return x, inside

    def _forward(self, x, grad: bool = False):
        t = torch.tensor(x, dtype=torch.float32)
        if grad:
            t.requires_grad_(True)
        out = self.model(t)
        z = out[:, 0].detach().numpy() if not grad else out[:, 0]
        e = out[:, 1]
        if not grad:
            P = 10 ** (z * (self._lp[1] - self._lp[0]) + self._lp[0])
            E = e.numpy() * (self._e[1] - self._e[0]) + self._e[0]
            return P, E
        return out, t

    # ------------------------------------------------------------------- API
    def predict(self, rho, T) -> tuple[np.ndarray, np.ndarray]:
        """Предсказание давления и удельной внутренней энергии.

        Args:
            rho: плотность, г/см^3, скаляр или массив.
            T: температура, К, скаляр или массив.

        Returns:
            (P, E): давление в ГПа и энергия в кДж/г, той же формы, что вход.

        Raises:
            ValueError: если rho или T <= 0.
        """
        x, _ = self._encode(rho, T)
        x2 = x.reshape(-1, 2)
        with torch.no_grad():
            out = self.model(torch.tensor(x2, dtype=torch.float32)).numpy()
        P = 10 ** (out[:, 0] * (self._lp[1] - self._lp[0]) + self._lp[0])
        E = out[:, 1] * (self._e[1] - self._e[0]) + self._e[0]
        shape = np.shape(rho)
        return P.reshape(shape), E.reshape(shape)

    def derivatives(self, rho, T) -> dict[str, np.ndarray]:
        """Частные производные и скорость звука в точке (ρ, T).

        Args:
            rho: плотность, г/см^3.
            T: температура, К.

        Returns:
            Словарь с ключами dP_drho [ГПа·см^3/г], dP_dT [ГПа/К],
            de_drho [кДж·см^3/(г^2)], de_dT [кДж/(г·К)] и cs [см/с].
        """
        x, _ = self._encode(rho, T)
        x2 = x.reshape(-1, 2)
        out, t = self._forward(x2, grad=True)
        gP = torch.autograd.grad(out[:, 0].sum(), t, retain_graph=True)[0].detach().numpy()
        ge = torch.autograd.grad(out[:, 1].sum(), t, retain_graph=True)[0].detach().numpy()

        lr = x2[:, 0] * (self._lr[1] - self._lr[0]) + self._lr[0]
        lt = x2[:, 1] * (self._lt[1] - self._lt[0]) + self._lt[0]
        rho_f, T_f = 10 ** lr, 10 ** lt
        o = out.detach().numpy()
        P = 10 ** (o[:, 0] * (self._lp[1] - self._lp[0]) + self._lp[0])
        e = o[:, 1] * (self._e[1] - self._e[0]) + self._e[0]

        s_lr = self._lr[1] - self._lr[0]
        s_lt = self._lt[1] - self._lt[0]
        dlnP_dlrho = gP[:, 0] * (self._lp[1] - self._lp[0]) / s_lr * np.log(10)
        dlnP_dlT = gP[:, 1] * (self._lp[1] - self._lp[0]) / s_lt * np.log(10)
        de_dlT = ge[:, 1] * (self._e[1] - self._e[0]) / s_lt

        dP_drho = P * dlnP_dlrho / (rho_f * np.log(10))
        dP_dT = P * dlnP_dlT / (T_f * np.log(10))
        de_dT = de_dlT / (T_f * np.log(10))
        cs2 = dP_drho * GPA_TO_CGS + T_f * (dP_dT * GPA_TO_CGS) ** 2 / \
            (rho_f ** 2 * np.maximum(de_dT * KJ_TO_CGS, 1e-8))
        return {"dP_drho": dP_drho, "dP_dT": dP_dT, "de_drho": np.zeros_like(de_dT),
                "de_dT": de_dT, "cs": np.sqrt(np.clip(cs2, 0, None)), "cs2": cs2}

    def sound_speed(self, rho, T) -> np.ndarray:
        """Скорость звука c_s(ρ, T).

        Args:
            rho: плотность, г/см^3.
            T: температура, К.

        Returns:
            Скорость звука в см/с (той же формы, что вход).
        """
        cs = self.derivatives(rho, T)["cs"]
        return cs.reshape(np.shape(rho))

    def check_physics(self, rho, T) -> dict[str, np.ndarray]:
        """Проверка термодинамических ограничений в точке (ρ, T).

        Args:
            rho: плотность, г/см^3.
            T: температура, К.

        Returns:
            Словарь флагов (bool-массивы): stable (∂P/∂ρ > 0),
            positive_heat_capacity (∂e/∂T > 0), causal_sound_speed (0 < c_s < c),
            in_domain (точка внутри табличного диапазона) и ok (все условия).
        """
        d = self.derivatives(rho, T)
        _, inside = self._encode(rho, T)
        stable = d["dP_drho"] > 0
        cap = d["de_dT"] > 0
        causal = (d["cs2"] > 0) & (d["cs"] < C_CGS)
        inside = inside.reshape(-1)
        ok = stable & cap & causal & inside
        shape = np.shape(rho)
        return {k: v.reshape(shape) for k, v in
                dict(stable=stable, positive_heat_capacity=cap,
                     causal_sound_speed=causal, in_domain=inside, ok=ok).items()}


if __name__ == "__main__":
    eos = EOSSurrogate()
    P, e = eos.predict(np.array([2.7, 0.5]), np.array([1e4, 1e6]))
    print("P, ГПа:", P, "| e, кДж/г:", e)
    print("cs, км/с:", eos.sound_speed(np.array([2.7, 0.5]), np.array([1e4, 1e6])) / 1e5)
    print("флаги:", eos.check_physics(np.array([2.7]), np.array([1e4])))
