from dataclasses import dataclass


@dataclass
class CellState:
    """
    State of a single lithium-ion cell.

    This is intentionally simple in v0.1
    Later versions will extend this with ECM status, RC voltages,
    hysteresis, parameter drift, and degradation states
    """

    soc: float
    voltage: float
    temparature: float
    soh: float
    capacity_ah: float
    internal_resistance_ohm: float


@dataclass
class CellConfig:
    v_min: float = 3.0
    v_max: float = 4.2
    capacity_ah: float = 3.4
    initial_temparature_c: float = 25.0
    initial_soh: float = 1.0
    internal_resistance_ohm: float = 0.02


def soc_to_voltage(soc: float, v_min: float = 3.0, v_max: float = 4.2) -> float:
    """
    Simple linear OCV approximation.

    This will later be replaced by an OCV-SOC lookup table or ECM model
    """
    soc = max(0.0, min(1.0, soc))
    return v_min + soc * (v_max - v_min)


def create_cell(soc: float, config: CellConfig | None = None) -> CellState:
    if config is None:
        config = CellConfig()

    voltage = soc_to_voltage(soc, config.v_min, config.v_max)

    return CellState(
        soc=soc,
        voltage=voltage,
        temparature=config.initial_temparature_c,
        soh=config.initial_soh,
        capacity_ah=config.capacity_ah,
        internal_resistance_ohm=config.internal_resistance_ohm
    )