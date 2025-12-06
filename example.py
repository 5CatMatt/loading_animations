import time

from loading_animations import *

RESET = "\033[0m"
RED = "\033[38;5;196m"
GREEN = "\033[38;5;46m"
BLUE = "\033[38;5;27m"
CYAN = "\033[38;5;51m"
YELLOW = "\033[38;5;226m"
MAGENTA = "\033[38;5;201m"

delay_time = 0.1
loop_count = 50

spinner = BrailleSpinner(text="Loading...", speed = 0.1, color = GREEN)

for counter in range(loop_count):
    spinner.update()
    time.sleep(delay_time)

spinner.finish()

loading_bar = GradientBar(
    start_color=(200, 15, 25),
    end_color=(0, 214, 17),
    length=50
)

bar_total = loop_count

for counter in range(bar_total):
    loading_bar.draw(counter + 1, bar_total)
    time.sleep(delay_time)

print("")

bar = RandomDotBar()

while not bar.is_complete():
    bar.update()
    time.sleep(0.03)

bar.finish()

print("")
                                             
progress_start, progress_end = 0, 100
new_bar = ProgressBarBraille(size = 10, color_dot = GREEN, color_border = RED, start = progress_start, end = progress_end)

for i in range(progress_start, progress_end + 1):
    time.sleep(delay_time)  # simulate work
    print("\r" + new_bar.set_progress(i), end="", flush=True)