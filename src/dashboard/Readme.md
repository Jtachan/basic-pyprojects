# Interactive sales dashboard

This project defines an interactive dashboard (graphs) constructed with [`bokeh`](https://bokeh.org/).
All the data displayed is defined as a SQL table, using [`sqlite3`](https://docs.python.org/3/library/sqlite3.html).

The database is coded so, whether the file "sales.db" previously exist or not, the data will always be overwritten to the default (displayed) data.
Each element in the table is defined by:

- Two categories: 'Electronics' and 'Clothing'
- Total revenue of sales.
- Date it was purchased.

