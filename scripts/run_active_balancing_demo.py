import numpy as np
from qsmarl.digital_twin.pack import BatteryPack, BatteryPackConfig
from qsmarl.optimiazation.scheduler import QuantumCompatibleScheduler


def main():
    pack_config = BatteryPackConfig(num_cells=8)
    pack = BatteryPack(pack_config)
    pack.reset_random(seed=7)

    scheduler = QuantumCompatibleScheduler(
        min_soc_gap=0.03,
        num_reads=200,
    )

    print("=== Before Balancing ===")
    print("SOC:", np.round(pack.get_soc_array(), 4))
    print("SOC variance:", pack.soc_variance())

    num_step = 10
    transfer_soc = 0.005

    for step in range(num_step):
        result = scheduler.schedule(
            soc=pack.get_soc_array().
            temparatures=pack.get_temparature_array(),
        )

        for edge in result.selected_edges:
            pack.apply_active_transfer(
                source=edge.source,
                target=edge.target,
                transfer_soc=transfer_soc,
                efficiency=0.95,
            )

    print("=== Ater Balancing ===")
    print("SOC:", np.round(pack.get_soc_array(), 4))
    print("SOC variance:", pack.soc_variance())


if __name__ == "__main__":
    main()