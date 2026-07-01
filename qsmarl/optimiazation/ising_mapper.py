from dataclasses import dataclass
import dimod

@dataclass
class IsingModel:
    h: dict[str, float]
    J: dict[tuple[str, str], float]
    offset: float