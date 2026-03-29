class TableStateMachine:
    def __init__(self, debounce_seconds=1.0):
        self.state = "EMPTY"
        self.last_empty_time = None
        self.last_change_time = 0
        self.debounce = debounce_seconds

        self.events = []

    def update(self, timestamp, person_present):
        # debounce защита
        if timestamp - self.last_change_time < self.debounce:
            return

        if self.state == "EMPTY" and person_present:
            self.state = "OCCUPIED"
            self.last_change_time = timestamp

            self.events.append(("APPROACH", timestamp))

            if self.last_empty_time is not None:
                delay = timestamp - self.last_empty_time
                self.events.append(("DELAY", delay))

        elif self.state == "OCCUPIED" and not person_present:
            self.state = "EMPTY"
            self.last_change_time = timestamp
            self.last_empty_time = timestamp

            self.events.append(("EMPTY", timestamp))