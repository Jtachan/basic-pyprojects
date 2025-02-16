"""Functions/Operations to display the information using Bokeh.

To run the code use the following command:
    bokeh serve --show graph.py
"""

from typing import Any

from bokeh import models, plotting, transform
from bokeh.io import curdoc
from bokeh.layouts import column, row
from database import init_table, fetch_data, TABLE_CATEGORIES

CATEGORY_OPTIONS = ["All", *TABLE_CATEGORIES]

# Fixme: The graph is correctly initialized, but it disappears when anything is modified.

# Initialize the data source:
init_table()
data = fetch_data()
source = models.ColumnDataSource(data)

# Create the plot:
plot = plotting.figure(
    title="Total sales by product", x_range=data["product"], height=400
)
plot.vbar(
    x="product",
    top="total_sales",
    width=0.9,
    source=source,
    fill_color=transform.factor_cmap(
        "product", "Category10_10", data["product"].unique()
    ),
)

# Widgets:
category_select = models.Select(title="Category", value="All", options=CATEGORY_OPTIONS)
date_range_slider = models.DateRangeSlider(
    title="Date range",
    value=("2023-10-01", "2023-10-06"),
    start="2023-10-01",
    end="2023-10-06",
)


def update_plot(attribute: str, old: Any, new: Any):
    """Callback function to update the plots.
    The plots are updated based on the selected options.

    While the input parameters are not explicitly used, they are part of Bokeh's
    callback mechanism, and they are communicated automatically to Bokeh.
    """
    category = category_select.value if category_select.value != "All" else None
    date_range = date_range_slider.value
    new_data = fetch_data(category=category, date_range=date_range)
    source.data = models.ColumnDataSource.from_df(new_data)
    plot.x_range.factors = new_data["product"]


# Attach callbacks to the widgets:
category_select.on_change("value", update_plot)
date_range_slider.on_change("value", update_plot)

# Layout & display:
layout = column(row(category_select, date_range_slider), plot)
curdoc().add_root(layout)
