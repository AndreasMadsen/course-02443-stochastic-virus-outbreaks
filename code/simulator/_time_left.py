
import time

class TimeLeft:
    def __init__(self, iterations, memory=0.9):
        self.average = 0

        self._total_iterations = iterations
        self._current_iteration = 0

        self._memory = memory
        self._first_iteration = True

    def _update_average(self, time):
        if self._first_iteration:
            self.average = time
            self._first_iteration = False
        else:
            self.average = self._memory * time + (1 - self._memory) * time

    def run(self, fn, *args, **kwargs):
        # Messure time usage
        start_time = time.time()
        fn(*args, **kwargs)
        end_time = time.time()
        time_usage = end_time - start_time

        # Update time usage
        self._update_average(time_usage)

        # Calculate remaining time
        self._current_iteration += 1
        iter_left = self._total_iterations - self._current_iteration
        time_left = self.average * iter_left

        return (time_usage, time_left)
