import sys
import time
import random

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

    def __init__(self, text = "Processing...", speed = 0.06, color = "\033[0m") -> None:
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
        self.color = color

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
        sys.stdout.write(f"\r {self.color} {frame} {self.text}")
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

class RandomDotBar:
    """
    A multi-slot terminal progress bar that fills each slot using a sequence of
    fractional Unicode braille block characters. Unlike linear progress bars,
    this bar fills in a *randomized* pattern.

    The bar consists of a fixed number of slots (`slots`). Each slot has a fill
    level ranging from 0 to 9, controlled by `dot_pattern`. A call to `update()`
    increments one random slot by one level until all slots reach maximum fill.

    Attributes:
        dot_pattern (list[str]):
            Unicode braille characters representing increasing fill density.
            Index 0 is empty (" "), index 9 is full ("⣿").

        slots (int):
            Total number of discrete chunks in the progress bar.

        levels (list[int]):
            Current fill level for each slot (0-9). Incremented randomly.

    Example:
        bar = RandomDotBar(slots=10)
        while not bar.is_complete():
            bar.update()
            time.sleep(0.03)
        bar.finish()
    """

    def __init__(self, slots=10) -> None:
        """
        Initialize the randomized progress bar.

        Args:
            slots (int, optional):
                Number of individual progress slots to render.
                Defaults to 10. Each slot fills independently.

        The constructor initializes each slot at level 0 (empty).

        Returns:
            None
        """
        # Characters representing increasing fill density.
        # These provide a smooth visual transition from empty → full.
        self.dot_pattern = [
            " ", "⡀", "⢐", "⣐", "⣰", "⣱", "⣳", "⣵", "⣷", "⣿"
        ]

        self.slots = slots

        # Track the fill level for each slot (initially all empty).
        # Levels range from 0 → 9, mapping into dot_pattern.
        self.levels = [0] * slots

    def update(self):
        """
        Increment a random slot by one level, then redraw the bar.

        Behavior:
            - Selects one slot at random (uniform selection).
            - Increments its fill level by 1.
            - Clamps the fill level to a valid range (max index 9).
            - Renders the updated bar in-place.

        Returns:
            None
        """
        # Randomly choose a slot to increment.
        idx = random.randint(0, self.slots - 1)

        # Increase fill level but clamp at maximum (⣿).
        max_level = len(self.dot_pattern) - 1
        self.levels[idx] = min(self.levels[idx] + 1, max_level)

        # Redraw the bar after update.
        self.draw()

    def draw(self):
        """
        Render the current state of the progress bar to the terminal.

        The bar is displayed in the format:
            [⣐⣰⢐⡀⣿⣿⣵⣐⣐⣀]

        Rendering uses `\r` to rewrite the same line in-place.

        Returns:
            None
        """
        # Convert level numbers into their matching Unicode characters.
        bar = "".join(self.dot_pattern[level] for level in self.levels)

        # Overwrite the current terminal line.
        sys.stdout.write(f"\r[{bar}]")
        sys.stdout.flush()

    def is_complete(self):
        """
        Check whether all slots have reached maximum fill.

        Returns:
            bool: True if every slot is filled to the highest level (⣿),
                  False otherwise.
        """
        max_level = len(self.dot_pattern) - 1
        return all(level == max_level for level in self.levels)

    def finish(self):
        """
        Finalize the bar output by printing a newline.

        Should be called after `is_complete()` returns True.

        Returns:
            None
        """
        sys.stdout.write("\n")
        sys.stdout.flush()

class ProgressBarBraille:
    """
    A braille-based progress bar that increments random slots while
    also tracking real completion percentage.

    Args:
        size (int): Number of character "slots" in the progress bar.
        dot_pattern (list[str]): List of unicode characters representing levels.
        color_dot (str): Optional ANSI color code to apply to the dots.
        color_border (str): Optional ANSI color code to apply brakets [].
    """

    def __init__(self, size=10, color_dot = None, color_border = None, start = 0, end = 100) -> None:
        self.size = size
        self.color_dot = color_dot or ""
        self.color_border = color_border or ""
        self.start = start
        self.end = end
        self.current = start

        self.dot_pattern = [
            " ", "⡀", "⢐", "⣐", "⣰", "⣱", "⣳", "⣵", "⣷", "⣿"
        ]

        self.levels = [0] * size  # holds which dot-pattern index each slot uses

    def set_progress(self, value):
        """
        Update the real progress value while animating random slot filling.

        Args:
            value (int or float): Current progress value between start and end.
        """
        # Clamp between start and end
        self.current = max(self.start, min(value, self.end))

        # Animate one random slot each update
        i = random.randint(0, self.size - 1)
        if self.levels[i] < len(self.dot_pattern) - 1:
            self.levels[i] += 1

        return self.render()

    def render(self):
        """
        Builds the current bar string using the dot pattern.

        Returns:
            str: The formatted progress bar: "[⡀⣐⣰   ]"
        """
        # If 100% done, force all slots to final symbol
        if self.current >= self.end:
            self.levels = [len(self.dot_pattern) - 1] * self.size

        dots = [
            self.color_dot + self.dot_pattern[level]
            for level in self.levels
        ]

        # Compute actual percentage
        total_range = self.end - self.start
        percent = ((self.current - self.start) / total_range) * 100 if total_range else 0

        current_pattern = self.color_border + "[" + "".join(dots) + self.color_border + f"]  {percent:5.1f}%"

        # # Compute actual percentage
        # current_pattern = self.color_border + "[" + "".join(dots) + self.color_border +"]"
        current_pattern += "\033[0m"  # Reset color at end

        return current_pattern
    