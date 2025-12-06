import time

from loading_animations import BrailleSpinner, GradientBar

delay_time = 0.1
loop_count = 50

spinner = BrailleSpinner()

for counter in range(loop_count):
    spinner.update()
    time.sleep(delay_time)

spinner.finish()

loading_bar = GradientBar(
    start_color=(0, 200, 255),
    end_color=(0, 50, 176),
    length=50
)

bar_total = loop_count

for counter in range(bar_total):
    loading_bar.draw(counter + 1, bar_total)
    time.sleep(delay_time)