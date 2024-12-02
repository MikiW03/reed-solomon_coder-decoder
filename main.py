from galois import Galois
from simulation import Simulation

if __name__ == '__main__':
    galois = Galois()
    galois.generate_generative_polynomial()

    sim = Simulation(galois)
    sim.start_simulation(100, [1, 2, 3, 6, 8, 12, 15, 25, 35, 45, 50, 55, 60, 100, 10000])
