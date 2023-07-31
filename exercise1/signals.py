import numpy as np
from astropy import units as u
from detect_duplicates import detect_duplicates


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
            intersections = detect_duplicates(list(self.signal[0] + other.signal[0]))
        elif axis == "y":
            intersections = detect_duplicates(list(self.signal[1] + other.signal[1]))
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
    time_array = np.arange(0, size) * 1e-5 * u.second

    # Sample Beam Signal
    beam_array = np.random.uniform(2 * 10e-3, 5 * 10e-3, size) * u.volt
    # Sample BPM Signal
    bpm_array = np.random.uniform(10e-3, 2 * 10e-3, size) * u.volt
    # Sample ADC signal
    adc_array = np.random.uniform(3 * 10e-3, 5 * 10e-3, size) * u.ampere

    Beam = Signal("Beam", np.array((time_array, beam_array)), frozenset((u.s, u.V)))
    Button_BPM = Signal("BPM", np.array((time_array, bpm_array)), frozenset((u.s, u.A)), duplicate_chance=0.1, axis='y')
    ADC = Signal("ADC", np.array((time_array, adc_array)), frozenset((u.s, u.V)), duplicate_chance=0.2, axis='both')

    signals = [Beam, Button_BPM, ADC]

    for signal in signals:
        print("\n\n\n")
        signal.display()
        duplicates = signal._detect_duplicates()
        print(signal.signal_type, "(axis=" + signal.axis + ") has ", len(duplicates), " duplicates:", duplicates)

    # Test two Beam signals for intersections in Voltage values (axis=y)

    # Sample signals for stripline and button beam position monitors
    bpm_array2 = np.random.uniform(0.98 * 10e-3, 1.98 * 10e-3, size) * u.volt
    Stripline_BPM = Signal("BPM", np.array((time_array, bpm_array2)), frozenset((u.s, u.V)))
    Stripline_BPM.signal_intersections(Beam, "y")
