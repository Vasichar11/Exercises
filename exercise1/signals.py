import numpy as np
from astropy import units as u
from detect_duplicates import detect_duplicates
import matplotlib.pyplot as plt
import pandas as pd


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
        if self._detect_duplicates() or other._detect_duplicates():
            raise ValueError("Signals have anomalies. To compare signals for intersection they should be free of duplicate values.")

        if axis == "x":
            intersections = detect_duplicates(list(self.signal[0]) + list(other.signal[0]))
        elif axis == "y":
            intersections = detect_duplicates(list(self.signal[1]) + list(other.signal[1]))
        else:
            raise ValueError("Invalid axis. Allowed values are 'x' or 'y'")

        return intersections

    def remove_duplicates(self, axis):
        df = pd.DataFrame({'x': self.signal[0], 'y': self.signal[1]})
        df.drop_duplicates(subset=axis, inplace=True)  # Will drop duplicates on specified axis
        self.signal = np.array((df['x'].values, df['y'].values))

    def display(self):
        print(f"Signal Type: {self.signal_type}")
        # print(f"Signal: {self.signal}")
        print(f"Units: {self.units}")
        print(f"Axis: {self.axis}")
        print(f"Duplicate Chance: {self.duplicate_chance}")


if __name__ == "__main__":
    # Parameters
    size = 100
    time_array = np.arange(0, size) * 1e-3
    low = 10e-3
    high = 2 * 10e-3
    num_intersections = 10

    beam_array = np.random.uniform(low, high, size)  # Sample Beam Signal
    button_array = np.random.uniform(low, high, size)  # Sample BPM Signals
    stripline_array = np.random.uniform(low, high, size)
    adc_array = np.random.uniform(low, high, size)  # Sample ADC signal

    # Introduce random intersections for BPM signals (needed for example 2)
    indices = np.random.choice(len(button_array), num_intersections, replace=False)
    for i in indices:  # Place the same random value at each selected index
        random_value = np.random.uniform(low, high)
        button_array[i] = random_value
        stripline_array[i] = random_value

    # Signal Instances
    Beam = Signal("Beam", np.array((time_array, beam_array)), frozenset((u.second, u.ampere)))
    Button_BPM = Signal("BPM", np.array((time_array, button_array)), frozenset((u.second, u.Volt)), duplicate_chance=0.1, axis='y')
    Stripline_BPM = Signal("BPM", np.array((time_array, stripline_array)), frozenset((u.s, u.V)))
    ADC = Signal("ADC", np.array((time_array, adc_array)), frozenset((u.second, u.Volt)), duplicate_chance=0.2, axis='y')
    ADC2 = Signal("ADC", np.array((time_array, adc_array)), frozenset((u.second, u.Volt)), duplicate_chance=0.2, axis='both')
    signals = [Beam, Button_BPM, ADC, ADC2]

    # Example 1: Test signals for anomalies (duplicates values)

    for signal in signals:
        print("\n\n\n")
        signal.display()
        duplicates = signal._detect_duplicates()
        print(signal.signal_type, "(axis=" + signal.axis + ") has ", len(duplicates), " duplicates:", duplicates)

    # Example 2: Test two Beam signals for intersections in Voltage (axis=y)

    Button_BPM.remove_duplicates(axis='y')  # Drop the previously introduced duplicates

    intersections = Stripline_BPM.signal_intersections(Button_BPM, "y")  # Compare y axis i.e. Voltage
    print("\n\nStripline and Button identical Voltages: ", intersections)

    ########################
    ########################
    ########################
    # Visualization Example 1
    ########################
    ########################
    ########################

    fig, ax = plt.subplots(2, 1)

    ax[0].plot(ADC.signal[0], ADC.signal[1], c='blue', label=ADC.signal_type)
    ax[0].set_xlabel(str(list(ADC.units)[0]))
    ax[0].set_ylabel(str(list(ADC.units)[1]))
    ax[0].set_title(ADC.signal_type)

    ax[1].plot(ADC.signal[0], ADC.signal[1], c='blue', label=ADC.signal_type)
    ax[1].set_xlabel(str(list(ADC.units)[0]))
    ax[1].set_ylabel(str(list(ADC.units)[1]))

    adc_duplicates = ADC._detect_duplicates()

    for time, voltage in zip(ADC.signal[0], ADC.signal[1]):
        if voltage in adc_duplicates:
            ax[1].scatter(time, voltage, c='red')

    # To avoid adding many labels
    if adc_duplicates:
        ax[1].scatter([], [], c='red', label='Duplicates')

    ax[0].legend(loc='lower right')
    ax[1].legend(loc='lower right')
    ax[0].grid()
    ax[1].grid()
    plt.show()

    ########################
    ########################
    ########################
    # Visualization Example 2
    ########################
    ########################
    ########################

    fig, ax = plt.subplots(3, 1)

    # Plot Stripline_BPM signal, Button_BPM signal, and both signals,  on separate subplots
    ax[0].plot(Stripline_BPM.signal[0], Stripline_BPM.signal[1], c='blue', label='Stripline_BPM')
    ax[1].plot(Button_BPM.signal[0], Button_BPM.signal[1], c='red', label='Button_BPM')

    ax[2].plot(Stripline_BPM.signal[0], Stripline_BPM.signal[1], c='blue', label='Stripline_BPM')
    ax[2].plot(Button_BPM.signal[0], Button_BPM.signal[1], c='red', label='Button_BPM')

    # Set labels
    ax[0].set_xlabel(str(list(Stripline_BPM.units)[0]))
    ax[1].set_xlabel(str(list(Button_BPM.units)[0]))
    ax[2].set_xlabel(str(list(Button_BPM.units)[0]))
    ax[0].set_ylabel(str(list(Stripline_BPM.units)[1]))
    ax[1].set_ylabel(str(list(Button_BPM.units)[1]))
    ax[2].set_ylabel(str(list(Button_BPM.units)[1]))

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

    for time, voltage in zip(Button_BPM.signal[0], Button_BPM.signal[1]):

        if voltage in intersections:
            ax[2].scatter(time, voltage, c='red', label='Intersections')

    for item in intersections:
        print(item in Stripline_BPM.signal[1])
        print(item in Button_BPM.signal[1])

    # Show the plot
    ax[0].grid(True)
    ax[1].grid(True)
    ax[2].grid(True)
    plt.tight_layout()
    plt.show()
