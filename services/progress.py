import time

class ProgressBar:
    """Displays a progress bar in the console."""
    def __init__(self):
        self.previous_sample = None

    def update(self, progress: int, total: int) -> None:
        """Updates the progress bar."""
        percent = 100 * (progress / float(total))
        bar = chr(9608) * int(percent) + "-" * (100 - int(percent))
        remaining_time = None if self.previous_sample is None else self.remaining_time(total - progress)
        print(
            f"\r|{bar}| {percent:.2f}% ( {progress} / {total} ) ETA: "
            f"{'N/A' if remaining_time is None else f'{remaining_time[0]}h {remaining_time[1]}m {remaining_time[2]}s'}",
            end="\r"
        )

    def sample_time(self):
        self.previous_sample = time.time() 

    def remaining_time(self, remaining):
        if self.previous_sample is None:
            raise Exception("Can't calculate elapsed time without any previous_sample")
        remaining_time = (time.time() - self.previous_sample) * remaining
 
        hours = int(remaining_time // 3600)
        minutes = int((remaining_time % 3600) // 60)
        seconds = int(remaining_time % 60)

        return (hours, minutes, seconds)
