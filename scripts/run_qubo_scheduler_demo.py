import numpy as np
from qsmarl.digital_twin.pack import BatteryPack, BatteryPackConfig


def main():
    pack_config = BatteryPackConfig(num_cells=8)
    pack = BatteryPack(pack_config)
    pack.reset_random(seed=42)

    print("=== Initial Pack State ===")
    print("=== Initial Pack State ===")


if __name__ == "__main__":
    main()