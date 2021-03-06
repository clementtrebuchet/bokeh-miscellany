from __future__ import print_function

from numpy import pi, sin, cos, linspace, tan

from bokeh.util.browser import view
from bokeh.document import Document
from bokeh.embed import file_html
from bokeh.models.glyphs import Line
from bokeh.models import (
    Plot, DataRange1d, LinearAxis, ColumnDataSource, Row, Column, Title
)
from bokeh.resources import INLINE

x = linspace(-2*pi, 2*pi, 1000)

source = ColumnDataSource(data = dict(
        x = x,
        y1 = sin(x),
        y2 = cos(x),
        y3 = tan(x),
        y4 = sin(x) * cos(x),
    )
)

MODE = 'box'


def make_plot(source, xname, yname, line_color, xdr=None, ydr=None, min_border=15, x_axis=True, y_axis=True, responsive=MODE, plot_width=600, plot_height=400):
    """ Returns a tuple (plot, [obj1...objN]); the former can be added
    to a GridPlot, and the latter is added to the plotcontext.
    """
    if not xdr:
        xdr = DataRange1d()
    if not ydr:
        ydr = DataRange1d()

    #title = Title(text='hello world', render_mode='canvas')

    plot = Plot(
        x_range=xdr, y_range=ydr,
        min_border=min_border,
        toolbar_location=None,
        responsive=responsive,
        plot_width=plot_width, plot_height=plot_height,
        title="Plot title",
    )

    if x_axis:
        plot.add_layout(LinearAxis(), 'below')
    if y_axis:
        plot.add_layout(LinearAxis(), 'left')

    plot.add_glyph(source, Line(x=xname, y=yname, line_color=line_color))

    return plot

plot1 = make_plot(source, "x", "y1", "blue", x_axis=False, y_axis=False, plot_width=200, plot_height=200)
plot2 = make_plot(source, "x", "y2", "red", xdr=plot1.x_range, y_axis=False)
plot3 = make_plot(source, "x", "y3", "green")
plot4 = make_plot(source, "x", "y4", "black")

grid = Column(
    Row(plot1, plot2, responsive=MODE),
    Row(plot3, plot4, responsive=MODE),
)

doc = Document()
doc.add_root(grid)

if __name__ == "__main__":
    filename = "row_column_plots.html"
    with open(filename, "w") as f:
        f.write(file_html(doc, INLINE, "Row Column Plots Example"))
    print("Wrote %s" % filename)
    view(filename)

