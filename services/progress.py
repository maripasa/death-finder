class ProgressBar:
    """Displays a progress bar in the console."""

    @staticmethod
    def update(progress: int, total: int) -> None:
        """Updates the progress bar."""
        percent = 100 * (progress / float(total))
        bar = chr(9608) * int(percent) + "-" * (100 - int(percent))
        print(f"\r|{bar}| {percent:.2f}% ( {progress} / {total} )", end="\r")
