import numpy as np
from qsmarl.digital_twin.pack import BatteryPack, BatteryPackConfig
from qsmarl.optimiazation.scheduler import QuantumCompatibleScheduler
from qsmarl.optimiazation.qubo_builder import QuboConfig

def main():
    pack_config = BatteryPackConfig(num_cells=8)
    pack = BatteryPack(pack_config)
    pack.reset_random(seed=42)

    print("=== Initial Pack State ===")
    print("SOC:", np.round(pack.get_soc_array(), 4))
    print("Temparature:", np.round(pack.get_temperature_array(), 4))
    print("SOC variance:", pack.soc_variance())

    scheduler = QuantumCompatibleScheduler(
        qubo_config=QuboConfig(
            alpha_gap_reward=10.0,
            beta_loss_penalty=1.0,
            gamma_thermal_penalty=0.5,
            lambda_one_source=20.0,
            lambda_one_target=20.0,
            lambda_max_edges=5.0,
            max_active_edges=2,
            efficiency=0.95
        ),
        min_soc_gap=0.03,
        num_reads=200,
    )

    result = scheduler.schedule(
        soc=pack.get_soc_array(),
        temparatures=pack.get_temperature_array(),
    )

    print("\n=== QUBO Scheduler Result ===")
    print("Energy:", result.energy)
    print("Sampler:", result.sample)

    print("\nSelected transfer edges:")
    for edge in result.selected_edges:
        print(
            f"cell {edge.source} -> cell {edge.target}, "
            f"SOC gap = {edge.soc_gap:.4f}"
        )

if __name__ == "__main__":
    main()