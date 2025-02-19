"""Functions/Operations to display the information using Bokeh.

To run the code use the following command:
    bokeh serve --show graph.py
"""

from typing import Any

from bokeh import plotting, transform
from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, Select, DateRangeSlider

from database import (
    init_table_with_default_values,
    get_date_range,
    fetch_total_sales_data,
    TABLE_CATEGORIES,
)

CATEGORY_OPTIONS = ["All", *TABLE_CATEGORIES]

# Initialize the data source:
init_table_with_default_values()
data = fetch_total_sales_data()
source = ColumnDataSource(data)

# Create the plot:
plot = plotting.figure(
    title="Total sales by product",
    x_range=data["product"],
    height=400,
    x_axis_label="Product",
    y_axis_label="Total Sales",
    tools="pan,wheel_zoom,box_zoom,reset",
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
min_date, max_date = get_date_range()
category_select = Select(title="Category", value="All", options=CATEGORY_OPTIONS)
date_range_slider = DateRangeSlider(
    title="Date range",
    value=(min_date, max_date),
    start=min_date,
    end=max_date,
)


def update_plot(_attribute: str, _old: Any, _new: Any):
    """Callback function to update the plots.
    The plots are updated based on the selected options.

    While the input parameters are not explicitly used, they are part of Bokeh's
    callback mechanism, and they are communicated automatically to Bokeh.
    """
    try:
        # Determine the category and date range:
        category = category_select.value if category_select.value != "All" else None
        date_range = tuple(str(v) for v in date_range_slider.value_as_date)

        # Fetch the new data:
        new_data = fetch_total_sales_data(category=category, date_range=date_range)
        if new_data.empty:
            raise ValueError("No data available for the selected filters.")

        # Validate data structure:
        required_columns = ["product", "total_sales"]
        if not all(col in new_data.columns for col in required_columns):
            raise ValueError(f"Missing required columns: {required_columns}")

        # Update ColumnDataSource:
        source.data = ColumnDataSource.from_df(new_data)
        # Update X- and Y-axis based on the new data.
        plot.x_range.factors = list(new_data["product"])
        max_sales = new_data["total_sales"].max()
        plot.y_range.end = 1 if max_sales == 0 else max_sales

    except Exception as e:
        print(f"Error updating the plot: {e}")


# Attach callbacks to the widgets:
category_select.on_change("value", update_plot)
date_range_slider.on_change("value", update_plot)

# Layout & display:
layout = column(row(category_select, date_range_slider), plot)
curdoc().add_root(layout)


if __name__ == "__main__":
    print("Hi")
