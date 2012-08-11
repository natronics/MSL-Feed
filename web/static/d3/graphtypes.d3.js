/**
 * Common Graph Class
 */
function Graph (cssClass, width, height) {
  this.cssClass   = cssClass;
  this.width      = width;
  this.height     = height;
}

Graph.prototype.set_data = function(data) {
  this.data = data;
}

/**
 * X Axis Class
 */
function XAxis (tics, labels) {
  this.tics   = tics;
  this.labels = labels;
  this.gutter = 16;
  this.min    = d3.min(tics);
  this.max    = d3.max(tics);
}

/**
 * X Axis Class
 */
function YAxis (tics, labels) {
  this.tics   = tics;
  this.labels = labels;
  this.gutter = 3;
  this.min    = d3.min(tics);
  this.max    = d3.max(tics);
}

/**
 * Draws a simple horizontal scale bar
 */
function PlainXAxis (graph, chart, axis) {
  this.paint = function (width) {
  
    var axis_scaler = d3.scale.linear()
        .domain([graph.xAxis.min, graph.xAxis.max])
        .range([graph.yAxis.gutter, width + 1]);

    // tics
    chart.append("line")
          .attr("x1", graph.yAxis.gutter)
          .attr("x2", axis_scaler(graph.xAxis.max) + 2)
          .attr("y1", graph.xAxis.gutter)
          .attr("y2", graph.xAxis.gutter)
          .attr("class", "xaxis_stroke");
    for (var i=0; i<graph.xAxis.tics.length; i++) {
      chart.append("line")
            .attr("x1", axis_scaler(graph.xAxis.tics[i])+1)
            .attr("x2", axis_scaler(graph.xAxis.tics[i])+1)
            .attr("y1", graph.xAxis.gutter)
            .attr("y2", graph.xAxis.gutter - 5)
            .attr("class", "xaxis_stroke");
    };
    
    // labels
    for (var i=0; i<graph.xAxis.tics.length; i++) {
      chart.append("g")
          .attr("x", axis_scaler(graph.xAxis.tics[i]) - graph.yAxis.gutter)
          .attr("y", 0)
          .attr("transform", "scale(1,-1)")
            .append("text")
              .attr("x", axis_scaler(graph.xAxis.tics[i]) - graph.yAxis.gutter)
              .attr("y", 0)
              .text(graph.xAxis.labels[i]);
    };
  }
}
