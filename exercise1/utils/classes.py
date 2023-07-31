# Test class for dates
class Date(object):
    def __init__(self, day, month, year):
        self.day, self.month, self.year = day, month, year

    def __eq__(self, other):  # Defines how classes should be compared for equality.
        if not isinstance(other, Date):  # Ensure they are both the same type
            return False
        return (self.year, self.month, self.day) == (other.year, other.month, other.day)

    def __hash__(self):
        return hash((self.year, self.month, self.day))

    def display_info(self):
        return f"{self.year} {self.month} {self.day}"


# Test class for proton particles
class Proton(object):
    def __init__(self, upar, Ekin, latitude, longitude):
        self.upar, self.Ekin, self.latitude, self.longitude = upar, Ekin, latitude, longitude

    def __eq__(self, other):  # Defines how classes should be compared for equality.
        if not isinstance(other, Proton):  # Ensure they are both the same type
            return False
        return (self.upar, self.Ekin, self.latitude, self.longitude) == (other.upar, other.Ekin, other.latitude, other.longitude)

    def __hash__(self):
        return hash((self.upar, self.Ekin, self.latitude, self.longitude))

    def display_info(self):
        return f"Parallel speed is {self.upar} with energy {self.Ekin} in latitude {self.latitude} degrees and longitude {self.longitude} degrees"
