"""Here are contained all Bokeh tutorials (from its website).
Each one is defined as its own function, named as the tutorial.
"""

import random

import numpy as np
from bokeh.layouts import layout, row
from bokeh.models import BoxAnnotation, Div, RangeSlider, Spinner
from bokeh.plotting import figure, show


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
    x = list(range(51))
    y = random.sample(range(100), 51)

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


def vectorizing_glyph_properties():
    """https://docs.bokeh.org/en/latest/docs/first_steps/first_steps_5.html"""
    size = 1000
    x = np.random.random(size=size) * 100
    y = np.random.random(size=size) * 100

    # Generation RGB hex colors in relation to 'y':
    radii = y / 100 * 2
    colors = [f"#{255:02x}{int(val * 255 / 100):02x}{255:02x}" for val in y]

    # Defining plot
    p = figure(
        title="Vectorized colors and radii example",
        sizing_mode="stretch_width",
        max_width=500,
        height=250,
    )
    p.circle(
        x, y, radius=radii, fill_color=colors, fill_alpha=0.6, line_color="lightgrey"
    )
    return p


def combining_plots() -> row:
    """https://docs.bokeh.org/en/latest/docs/first_steps/first_steps_6.html"""
    x = list(range(11))
    y1 = [10 - i for i in x]
    y2 = [abs(i - 5) for i in x]

    # Creating three plots, one for each rendering:
    s1 = figure(width=250, height=250, background_fill_color="#fafafa")
    s2 = figure(width=250, height=250, background_fill_color="#fafafa")
    s3 = figure(width=250, height=250, background_fill_color="#fafafa")

    s1.scatter(x, x, marker="circle", size=12, color="grey", alpha=0.8)
    s2.scatter(x, y1, marker="triangle", size=12, color="green", alpha=0.8)
    s3.scatter(x, y2, marker="square", size=12, color="red", alpha=0.8)

    return row(children=[s1, s2, s3], sizing_mode="scale_width")


def using_widgets() -> layout:
    """https://docs.bokeh.org/en/latest/docs/first_steps/first_steps_9.html"""
    x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    y = [4, 5, 5, 7, 2, 6, 4, 9, 1, 3]

    p = figure(x_range=(1, 9), width=500, height=250)
    points = p.scatter(x=x, y=y, size=30, fill_color="#21a7df")

    div = Div(
        text="Select the circle's size using this control element:",
        width=200,
        height=30,
    )
    spinner = Spinner(
        title="Circle size", low=0, high=60, step=5, value=points.glyph.size, width=200
    )
    spinner.js_link("value", points.glyph, "size")
    range_slider = RangeSlider(
        title="Adjust x-axis range",
        start=0,
        end=len(x),
        step=1,
        value=(p.x_range.start, p.x_range.end),
    )
    range_slider.js_link("value", p.x_range, "start", attr_selector=0)
    range_slider.js_link("value", p.x_range, "end", attr_selector=1)
    return layout([[div, spinner], [range_slider], [p]])


if __name__ == "__main__":
    bokeh_plot = using_widgets()
    show(bokeh_plot)
