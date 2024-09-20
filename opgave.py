class opgave:
    def __init__(self, opgavenum, hovedeopgave, ekstraopgave):
        self._opgavenum = opgavenum
        self._hovedeopgave = hovedeopgave
        self._ekstraopgave = ekstraopgave

    @property
    def opgavenum(self):
        return self._opgavenum

    @property
    def hovedeopgave(self):
        return self._hovedeopgave

    @property
    def ekstraopgave(self):
        return self._ekstraopgave