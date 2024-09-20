class opgaveholdnummer:
    def __init__(self, opgavenum, holdnummer, hovedeopgave, ekstraopgave):
        self._opgavenum = opgavenum
        self._holdnummer = holdnummer
        self._hovedeopgave = hovedeopgave
        self._ekstraopgave = ekstraopgave

    # Getter methods
    def get_opgavenum(self):
        return self._opgavenum

    def get_holdnummer(self):
        return self._holdnummer

    def get_hovedeopgave(self):
        return self._hovedeopgave

    def get_ekstraopgave(self):
        return self._ekstraopgave

    # Setter methods
    def set_opgavenum(self, opgavenum):
        self._opgavenum = opgavenum

    def set_holdnummer(self, holdnummer):
        self._holdnummer = holdnummer

    def set_hovedeopgave(self, hovedeopgave):
        self._hovedeopgave = hovedeopgave

    def set_ekstraopgave(self, ekstraopgave):
        self._ekstraopgave = ekstraopgave

    # Method to calculate total points
    def calculate_total_points(self):
        if (self._ekstraopgave == -1):
            return self._hovedeopgave
        elif (self._hovedeopgave == -1):
            return self._ekstraopgave
        else:
            return self._hovedeopgave + self._ekstraopgave