# Interactive sales dashboard

This project defines an interactive dashboard (graphs) constructed with [`bokeh`](https://bokeh.org/).
All the data displayed is defined as a SQL table, using [`sqlite3`](https://docs.python.org/3/library/sqlite3.html).

The database is coded so, whether the file "sales.db" previously exist or not, the data will always be overwritten to the default (displayed) data.
Each element in the table is defined by:

- Two categories: 'Electronics' and 'Clothing'
- Total revenue of sales.
- Date it was purchased.

[`Bokeh`](https://bokeh.org/) is then used as the backend to plot all the information, as a vertical bar graph, on an html interactive file.
This is launched with the following command:

```commandline
bokeh serve --show graph.py
```

The graph displays the ammount of sales as the Y-axis and the product on the X-axis.
It also allows filtering by:

- Product category.
- Range of purchase date.
