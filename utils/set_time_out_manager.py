import threading

class SetTimeoutManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.timers = []
        return cls._instance

    def setTimeout(self, func, delay):
        timer = threading.Timer(delay, func)
        timer.start()
        self.timers.append(timer)
        return timer

    def clearTimeout(self, timer):
        if timer in self.timers:
            timer.cancel()
            self.timers.remove(timer)
        else:
            print("Timer not found.")

    def clearAllTimeouts(self):
        for timer in self.timers:
            timer.cancel()
        self.timers.clear()