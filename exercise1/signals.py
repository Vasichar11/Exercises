import numpy as np
from astropy import units as u
from detect_duplicates import detect_duplicates
import matplotlib.pyplot as plt


# Class for signals
class Signal:
    def __init__(self, signal_type, signal, units=frozenset(), duplicate_chance=0, axis="y"):
        if duplicate_chance < 0 or duplicate_chance > 1:
            raise ValueError("Invalid duplicate_chance argument. Allowed values are between '0' and '1'.")
        if axis not in ["x", "y", "both", None]:
            raise ValueError("Invalid axis. Allowed values are 'x' or 'y' or None.")
        self.signal_type = signal_type
        self.signal = signal
        self.units = units
        self.duplicate_chance = duplicate_chance
        self.axis = axis
        self.introduce_duplicates()

    # Class-specific detection on desired axis
    def _detect_duplicates(self):
        duplicates = []
        if self.axis == "x" or self.axis == "both":
            duplicates.extend(detect_duplicates(list(self.signal[0])))
        if self.axis == "y" or self.axis == "both":
            duplicates.extend(detect_duplicates(list(self.signal[1])))

        return duplicates

    # Function that introduces duplicates with a probability
    def introduce_duplicates(self):
        modifying_signals = []
        if self.axis == "x" or self.axis == "both":
            modifying_signals.append(self.signal[0])
        if self.axis == "y" or self.axis == "both":
            modifying_signals.append(self.signal[1])

        for signal in modifying_signals:
            if self.duplicate_chance != 0:
                size = len(signal)
                num_duplicates = int(size * self.duplicate_chance)

                if num_duplicates > 0:
                    indices = np.random.choice(size, num_duplicates, replace=False)
                    signal[indices] = np.random.choice(signal, num_duplicates)

    # Function to find intersections between two signals of the same type
    def signal_intersections(self, other, axis):
        if not isinstance(other, Signal):
            raise ValueError("Input must be a Signal object.")
        if self.signal_type != other.signal_type:
            raise ValueError("Signals must be of the same type for comparison.")
        if axis == "x":
            intersections = detect_duplicates(list(self.signal[0]) + list(other.signal[0]))
        elif axis == "y":
            intersections = detect_duplicates(list(self.signal[1]) + list(other.signal[1]))
        else:
            raise ValueError("Invalid axis. Allowed values are 'x' or 'y'")

        return intersections

    def display(self):
        print(f"Signal Type: {self.signal_type}")
        print(f"Signal: {self.signal}")
        print(f"Units: {self.units}")
        print(f"Axis: {self.axis}")
        print(f"Duplicate Chance: {self.duplicate_chance}")


if __name__ == "__main__":

    size = 100
    time_array = np.arange(0, size) * 1e-5

    # Sample Beam Signal
    beam_array = np.random.uniform(2 * 10e-3, 5 * 10e-3, size)
    # Sample BPM Signal
    bpm_array = np.random.uniform(10e-3, 2 * 10e-3, size)
    # Sample ADC signal
    adc_array = np.random.uniform(3 * 10e-3, 5 * 10e-3, size)

    Beam = Signal("Beam", np.array((time_array, beam_array)), frozenset((u.second, u.ampere)))
    Button_BPM = Signal("BPM", np.array((time_array, bpm_array)), frozenset((u.second, u.Volt)), duplicate_chance=0.1, axis='y')
    ADC = Signal("ADC", np.array((time_array, adc_array)), frozenset((u.second, u.Volt)), duplicate_chance=0.2, axis='both')

    signals = [Beam, Button_BPM, ADC]

    # Example 1: Test signals for anomalies (duplicates values)

    for signal in signals:
        print("\n\n\n")
        signal.display()
        duplicates = signal._detect_duplicates()
        print(signal.signal_type, "(axis=" + signal.axis + ") has ", len(duplicates), " duplicates:", duplicates)

    # Example 2: Test two Beam signals for intersections in Voltage (axis=y)

    # Comparing button and stripline BPM signals
    bpm_array2 = np.random.uniform(0.999 * 10e-3, 1.9999 * 10e-3, size)
    Stripline_BPM = Signal("BPM", np.array((time_array, bpm_array2)), frozenset((u.s, u.V)))

    intersections = Stripline_BPM.signal_intersections(Button_BPM, "y")

    print("\n\nStripline and Button identical Voltages: ", intersections)

    ########################
    ########################
    ########################
    # Visualization
    ########################
    ########################
    ########################

    fig, ax = plt.subplots(3, 1)  # 2 rows, 1 column

    # Plot Stripline_BPM and Button_BPM signals on separate subplots
    ax[0].plot(Stripline_BPM.signal[0], Stripline_BPM.signal[1], c='blue', label='Stripline_BPM')
    ax[1].plot(Button_BPM.signal[0], Button_BPM.signal[1], c='red', label='Button_BPM')

    # Set labels
    ax[0].set_xlabel(str(list(Stripline_BPM.units)[0]))
    ax[1].set_xlabel(str(list(Button_BPM.units)[0]))
    ax[0].set_ylabel(str(list(Stripline_BPM.units)[1]))
    ax[1].set_ylabel(str(list(Button_BPM.units)[1]))

    # Set limits
    x_min = min(min(Stripline_BPM.signal[0]), min(Button_BPM.signal[0]))
    x_max = max(max(Stripline_BPM.signal[0]), max(Button_BPM.signal[0]))
    y_min = min(min(Stripline_BPM.signal[1]), min(Button_BPM.signal[1]))
    y_max = max(max(Stripline_BPM.signal[1]), max(Button_BPM.signal[1]))
    ax[0].set_xlim([x_min, x_max])
    ax[1].set_xlim([x_min, x_max])
    ax[2].set_xlim([x_min, x_max])
    ax[0].set_ylim([y_min, y_max])
    ax[1].set_ylim([y_min, y_max])
    ax[2].set_ylim([y_min, y_max])

    # Set ticks
    x_ticks = np.linspace(x_min, x_max, 5)
    y_ticks = np.linspace(y_min, y_max, 5)
    ax[0].set_xticks(x_ticks)
    ax[1].set_xticks(x_ticks)
    ax[2].set_xticks(x_ticks)
    ax[0].set_yticks(y_ticks)
    ax[1].set_yticks(y_ticks)
    ax[2].set_yticks(y_ticks)

    # Set titles and legends
    ax[0].set_title('Stripline_BPM Signal')
    ax[1].set_title('Button_BPM Signal')
    ax[2].set_title('Signal intersections')
    print(intersections)
    for time, voltage in zip(Button_BPM.signal[0], Button_BPM.signal[1]):
        if voltage in intersections:
            ax[2].scatter(time, voltage, c='red', label='Intersections')

    # Show the plot
    ax[0].grid(True)
    ax[1].grid(True)
    ax[2].grid(True)
    plt.tight_layout()  # Adjusts subplot parameters to give specified padding.
    plt.show()
