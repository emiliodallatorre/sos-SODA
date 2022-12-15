from tqdm import tqdm

from models.planet import Planet
from models.system import System
from models.vector import Vector
from utils.benchmark import Benchmark

system: System = System(
    [
        Planet(
            "Sun",
            1,
            Vector(0, 0, 0),
            Vector(0, 0, 0),
            "yellow",
            True,
        ),
        Planet(
            "Earth",
            1 / 2,
            Vector(4, 0, 0),
            Vector(0, 1 / 2, 0),
            "blue",
        ),
        # Planet(
        #    "Moon",
        #    1 / 2000,
        #    Vector(4 + 0.04 * sqrt(2) / 2, 0, 0.04 * sqrt(2) / 2),
        #    Vector(-5 / sqrt(2) * sqrt(2) / 2, 1 / 2, 5 / sqrt(2) * sqrt(2) / 2),
        #    "gray",
        # ),
    ],
    G=1,
)

dt: int = 1
steps: int = 1000


def simulate_with_opencl():
    simulation_results: list = system.simulate_with_opencl(dt, steps)
    system.simulate(dt, steps)
    # from plotter import Plotter
    # plotter: Plotter = Plotter(simulation_results, dt, steps)
    # plotter.plot()


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

simulate_with_opencl()