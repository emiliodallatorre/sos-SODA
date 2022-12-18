from tqdm import tqdm

import references
from models.system import System
from utils.benchmark import Benchmark

system: System = System(
    references.dots,
    G=1,
)

dt: float = 0.001
steps: int = 1000


def simulate(opencl: bool):
    if opencl:
        simulation_results: list = system.simulate_with_opencl(dt, steps)
    else:
        simulation_results: list = system.simulate(dt, steps)

    from plotter import Plotter
    plotter: Plotter = Plotter(simulation_results, dt, steps)
    plotter.plot()


def benchmark():
    cpu_benchmarks: list = []
    gpu_benchmarks: list = []
    steps: list = []

    for i in tqdm(range(1000, 10000, 1000)):
        cpu_benchmark: Benchmark = Benchmark(system.simulate, dt, i)
        gpu_benchmark: Benchmark = Benchmark(system.simulate_with_opencl, dt, i)

        cpu_benchmark.run()
        gpu_benchmark.run()

        cpu_benchmarks.append(cpu_benchmark)
        gpu_benchmarks.append(gpu_benchmark)

        steps.append(i)

    cpu_times: list = [benchmark.time for benchmark in cpu_benchmarks]
    gpu_times: list = [benchmark.time for benchmark in gpu_benchmarks]

    # Plot the results
    import matplotlib.pyplot as plt

    plt.plot(steps, cpu_times, label="CPU")
    plt.plot(steps, gpu_times, label="GPU")
    plt.xlabel("Steps")
    plt.ylabel("Time (ms)")
    plt.legend()
    plt.show()


def benchmark_difference():
    cpu_states: list = system.simulate(dt, steps)
    gpu_states: list = system.simulate_with_opencl(dt, steps)

    differences: list = []
    for i in range(steps):
        difference: float = 0
        for j in range(len(cpu_states[i])):
            # Print CPU and GPU position
            difference += cpu_states[i][j].position.distance(gpu_states[i][j].position)

        print(difference)
        differences.append(difference)

    import matplotlib.pyplot as plt

    plt.plot(range(steps), differences)
    plt.xlabel("Step")
    plt.ylabel("Difference")
    plt.legend()
    plt.show()


benchmark_difference()
