import numpy as np
from qsmarl.digital_twin.pack import BatteryPack, BatteryPackConfig
from qsmarl.optimiazation.scheduler import Q

def main():
    pack_config = BatteryPackConfig(num_cells=8)
    pack = BatteryPack(pack_config)
    pack.reset_random(seed=42)

    print("=== Initial Pack State ===")
    print("SOC:", np.round(pack.get_soc_array(), 4))
    print("Temparature:", np.round(pack.get_temperature_array(), 4))
    print("SOC variance:", pack.soc_variance())

    scheduler = QuantumCompatibleScheduler(

    )


if __name__ == "__main__":
    main()