"""Here are contained all Bokeh tutorials (from its website).
Each one is defined as its own function, named as the tutorial.
"""

import random
from bokeh.plotting import figure, show
from bokeh.models import BoxAnnotation


def create_a_simple_line_chart() -> figure:
    """https://docs.bokeh.org/en/latest/docs/first_steps/first_steps_1.html

    Modification
    ------------
    The 'Combining multiple graphs' section is not included here. The reason is that
    is also clearly shown at the exercise #2.
    """
    # Preparing some data:
    x = [1, 2, 3, 4, 5]
    y = [6, 7, 3, 4, 5]
    # Creating a new plot figure:
    fig = figure(title="Simple line example", x_axis_label="x", y_axis_label="y")
    # Adding a line to render:
    fig.line(x, y, legend_label="Temp.", line_width=2)
    return fig


def rendering_different_glyphs() -> figure:
    """https://docs.bokeh.org/en/latest/docs/first_steps/first_steps_2.html

    Modification
    ------------
    Each new plot is drawn on top of the previous ones. For better visualisation, the
    order of the plots has been rearranged so the line plot is on top of the bars.
    """
    # Data:
    x = [1, 2, 3, 4, 5]
    y1 = [6, 7, 2, 4, 5]
    y2 = [2, 3, 4, 5, 6]
    y3 = [4, 5, 5, 7, 2]
    # Creating figure plot:
    p = figure(title="Multiple glyphs example", x_axis_label="x", y_axis_label="y")
    # Adding multiple renders: line, vertical bar and scatter points
    p.vbar(x, top=y2, legend_label="Rate", color="red", width=0.5, bottom=0)
    p.line(x, y1, legend_label="Temp", color="#004488", line_width=3)
    p.scatter(x, y3, legend_label="Objects", color="yellow", size=12)

    return p


def adding_legends_text_annotations() -> figure:
    """https://docs.bokeh.org/en/latest/docs/first_steps/first_steps_3.html

    Modifications
    -------------
    This single example takes all the changes from the three examples into a single
    one. There are some changes that are skipped to keep the final plot clearer.
    """
    x = list(range(0, 51))
    y = random.sample(range(0, 100), 51)

    plot = figure(title="Legend and headline example with box annotation")

    # Operations over the headline:
    plot.title_location = "left"
    plot.title.text_font_size = "25px"
    plot.title.align = "right"
    plot.title.background_fill_color = "darkgrey"
    plot.title.text_color = "white"

    # Add circle rendered with 'legend_label' arguments:
    plot.line(x, y, legend_label="Temp", line_color="blue", line_width=2)

    # Operations over the legend:
    legend = plot.legend
    # Adding a title to the legend:
    legend.title = "Observations"
    # Change appearance of legend text:
    legend.label_text_font = "times"
    legend.label_text_font_style = "italic"
    legend.label_text_color = "navy"
    # Change border and background of legend:
    legend.border_line_width = 3
    legend.border_line_color = "navy"
    legend.border_line_alpha = 0.8
    legend.background_fill_color = "navy"
    legend.background_fill_alpha = 0.2

    # Box annotations:
    low_box = BoxAnnotation(top=20, fill_alpha=0.2, fill_color="#F0E442")
    mid_box = BoxAnnotation(bottom=20, top=80, fill_alpha=0.2, fill_color="#009E73")
    high_box = BoxAnnotation(bottom=80, fill_alpha=0.2, fill_color="#F0E442")

    for box in (low_box, mid_box, high_box):
        plot.add_layout(box)

    return plot


if __name__ == "__main__":
    f = adding_legends_text_annotations()
    show(f)
