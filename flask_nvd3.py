# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 19:22:10 2014

@author: sagar
"""
from nvd3 import pieChart
from flask import Flask, send_from_directory

from os.path import join

def generate_nvd3_html():
    #Open File to write the D3 Graph
    output_file_path = 'test-nvd3.html'
    output_file = open(output_file_path, 'w')
    
    type = 'pieChart'
    chart = pieChart(name=type, color_category='category20c', height=450, width=450)
    chart.set_containerheader("\n\n<h2>" + type + "</h2>\n\n")
    
    #Create the keys
    xdata = ["Orange", "Banana", "Pear", "Kiwi", "Apple", "Strawberry", "Pineapple"]
    ydata = [3, 4, 0, 1, 5, 7, 3]
    
    #Add the series
    extra_serie = {"tooltip": {"y_start": "", "y_end": " cal"}}
    chart.add_serie(y=ydata, x=xdata, extra=extra_serie)
    chart.buildhtml()
    output_file.write(chart.htmlcontent)
    
    #close Html file
    output_file.close()
    
    return output_file_path
    
app = Flask(__name__)

@app.route("/")
def hello():
    html_file_path = generate_nvd3_html()
    return send_from_directory('web','test-nvd3.html')

if __name__ == "__main__":
    app.run(host='127.0.0.1', debug=True, use_reloader=False)