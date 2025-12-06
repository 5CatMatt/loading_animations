import sys
import time

class BrailleSpinner:
    """
    A lightweight, non-blocking terminal spinner that uses braille Unicode
    characters to render a smooth animation. This class is designed to be
    updated repeatedly inside long-running loops.

    The spinner only updates when the specified time interval has passed,
    preventing excessive terminal writes and providing visually stable output.
    """
    frames = [
        "⠁", "⠂", "⠄", "⡀", "⢀", "⠠", "⠐", "⠈"
    ]

    def __init__(self, text="Processing...", speed = 0.06) -> None:
        """
        BrailleSpinner instance.

        Args:
            text (str): Text displayed beside the spinner animation.
                        Defaults to "Processing...".
            speed (float): Minimum delay between animation frame updates, in seconds.
                           A lower value results in a faster animation. Default is 0.06.
        
        Returns:
            None
        """
        self.text = text
        self.speed = speed
        self.last_update = 0
        self.index = 0

    def update(self) -> None:
        """
        Update the spinner animation. This method should be called once per loop iteration.

        The update is non-blocking: if insufficient time has passed since the
        last update, the function returns immediately without writing to stdout.

        Args:
            None

        Returns:
            None
        """
        now = time.time()

        # Control animation speed
        if now - self.last_update < self.speed:
            return
        
        self.last_update = now

        # Advance animation frame
        self.index = (self.index + 1) % len(self.frames)
        frame = self.frames[self.index]

        # Print the spinner on the same line
        sys.stdout.write(f"\r{frame} {self.text}")
        sys.stdout.flush()

    def finish(self) -> None:
        """
        Finalize the spinner display by clearing the animation and printing a completion message.

        Args:
            None
            
        Returns:
            None
        """
        sys.stdout.write("\r✔ Done!            \n")
        sys.stdout.flush()

class GradientBar:
    def __init__(self, start_color=(255, 0, 0), end_color=(0, 128, 255), length=40) -> None:
        """
        Initialize a new GradientBar instance.

        Args:
            start_color (tuple[int, int, int]): RGB tuple (0–255 each) for the left side color.
            end_color   (tuple[int, int, int]): RGB tuple for the right side color.
            length (int): Number of character blocks used to render the bar.
        
        Returns:
            None
        """
        self.start_r, self.start_g, self.start_b = start_color
        self.end_r, self.end_g, self.end_b = end_color
        self.length = length

    def _interp_color(self, t) -> tuple[int, int, int]:
        """
        Compute an interpolated RGB color between the start and end colors.

        Args:
            t (float): Normalized position in the gradient (0.0 = start, 1.0 = end).

        Returns:
            tuple[int, int, int]: Interpolated (R, G, B) color values.
        """
        r = int(self.start_r + (self.end_r - self.start_r) * t)
        g = int(self.start_g + (self.end_g - self.start_g) * t)
        b = int(self.start_b + (self.end_b - self.start_b) * t)
        return r, g, b

    def draw(self, current, total) -> None:
        """
        Render the progress bar for the given progress state.
        Updates in-place using '\r'

        Args:
            current (int): Current progress value.
            total   (int): Maximum progress value.

        Returns:
            None
        """
        if total == 0:
            percent = 0
        else:
            percent = current / total

        filled_len = int(self.length * percent)

        bar = ""

        # Build gradient fill
        for i in range(self.length):
            t = i / max(self.length - 1, 1)
            r, g, b = self._interp_color(t)

            if i < filled_len:
                bar += f"\x1b[48;2;{r};{g};{b}m \x1b[0m"   # colored block
            else:
                bar += f"\x1b[48;2;30;30;30m \x1b[0m"       # background empty block

        sys.stdout.write(f"\r{bar} {percent * 100:5.1f}%")
        sys.stdout.flush()

    def finish(self) -> None:
        """
        Finalize the progress bar by advancing to a new line.

        Args:
            None

        Returns:
            None
        """
        sys.stdout.write("\n")
        sys.stdout.flush()