import matplotlib.pyplot as plt
import py_dss_interface
import os
import pathlib
import numpy as np

# DSS dosyasının bulunduğu dizini ve dosya adını ayarlayın
script_path = os.path.dirname(os.path.abspath(__file__))
dss_file = pathlib.Path(script_path).joinpath("feeders", "13bus", "IEEE13Nodeckt.dss")

# OpenDSS'yi başlatın
dss = py_dss_interface.DSS()

# DSS dosyasını derleyin
dss.text(f"compile [{dss_file}]")

# Rastgele tap değeri üretmek için fonksiyon
def generate_random_tap_value():
    return np.random.randint(-16, 17)  # Adjusted range to include both -16 and 16

# Grey Wolf Optimizer (GWO) Algorithm with enhancements
def gwo_optimizer(max_iter=3000, num_wolves=10):
    num_transformers = dss.transformers.count
    num_dimensions = num_transformers

    # Initialization
    alpha_pos = np.zeros(num_dimensions)
    beta_pos = np.zeros(num_dimensions)
    delta_pos = np.zeros(num_dimensions)

    alpha_score = float("inf")
    beta_score = float("inf")
    delta_score = float("inf")

    positions = np.zeros((num_wolves, num_dimensions))
    scores = np.zeros(num_wolves)

    for i in range(num_wolves):
        positions[i, :] = [generate_random_tap_value() for _ in range(num_dimensions)]

    # Main loop
    for iteration in range(1, max_iter + 1):
        a = 2 - iteration * (2 / max_iter)  # Linearly decreased from 2 to 0

        # Update positions
        for i in range(num_wolves):
            for j in range(num_dimensions):
                r1 = np.random.random()  # Random number between 0 and 1
                r2 = np.random.random()

                A1 = 2 * a * r1 - a
                C1 = 2 * r2

                D_alpha = abs(C1 * alpha_pos[j] - positions[i, j])
                X1 = alpha_pos[j] - A1 * D_alpha

                r1 = np.random.random()
                r2 = np.random.random()

                A2 = 2 * a * r1 - a
                C2 = 2 * r2

                D_beta = abs(C2 * beta_pos[j] - positions[i, j])
                X2 = beta_pos[j] - A2 * D_beta

                r1 = np.random.random()
                r2 = np.random.random()

                A3 = 2 * a * r1 - a
                C3 = 2 * r2

                D_delta = abs(C3 * delta_pos[j] - positions[i, j])
                X3 = delta_pos[j] - A3 * D_delta

                positions[i, j] = (X1 + X2 + X3) / 3

                # Boundary enforcement
                if positions[i, j] > 16:
                    positions[i, j] = 16
                elif positions[i, j] < -16:
                    positions[i, j] = -16

        # Calculate scores
        for i in range(num_wolves):
            tap_values = dict(zip(dss.transformers.names, positions[i]))
            update_transformer_taps(tap_values)
            dss.text("solve")

            # Calculate score (total distance to 1)
            voltages = get_node_voltages()
            scores[i] = sum(abs(v - 1) for v in voltages)

        # Update alpha, beta, and delta
        best_index = np.argmin(scores)
        if scores[best_index] < alpha_score:
            alpha_score = scores[best_index]
            alpha_pos = positions[best_index, :].copy()

        positions = np.sort(positions, axis=0)
        alpha_pos = positions[0, :].copy()
        beta_pos = positions[1, :].copy()
        delta_pos = positions[2, :].copy()

        # Print iteration info
        if iteration % 100 == 0:
            print(f"Iteration: {iteration}, Best Score: {alpha_score}")

    return alpha_pos, alpha_score

# Function to update transformer taps
def update_transformer_taps(tap_values):
    for transformer_name, tap_value in tap_values.items():
        dss.transformers.name = transformer_name
        dss.transformers.tap = tap_value

# Function to get node voltages
def get_node_voltages():
    voltages = []
    for phase in range(1, 4):
        voltages.extend(dss.circuit.nodes_vmag_pu_by_phase(phase))
    return voltages

# Main function
def main():
    # Call GWO optimizer with enhancements
    best_tap_values, min_distance = gwo_optimizer(max_iter=3000, num_wolves=20)

    # Print results
    print("En küçük uzaklık:", min_distance)
    print("En iyi tap değerleri:", best_tap_values)

    # Plotting (if needed)

if __name__ == "__main__":
    main()
