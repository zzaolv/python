# chart_display.py
import matplotlib.pyplot as plt
import pandas as pd

def generate_chart(data, chart_type, x_column, y_column, output_filename):
    if chart_type == 'bar':
        data.plot.bar(x=x_column, y=y_column)
    elif chart_type == 'line':
        data.plot.line(x=x_column, y=y_column)
    elif chart_type == 'scatter':
        data.plot.scatter(x=x_column, y=y_column)
    else:
        raise ValueError('Invalid chart type')

    plt.savefig(output_filename)
    plt.close()
