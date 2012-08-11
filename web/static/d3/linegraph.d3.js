/**
 * Horizontal Line Chart Class
 */
function HLine (css, w, h) {
  this.graph      = new Graph(css, w, h);
  
  this.set_xAxis = function (axis) {
    this.graph.xAxis = axis;
  };
  
  this.set_yAxis = function (axis) {
    this.graph.yAxis = axis;
  };
  
  this.show = function (id) {
    this.domid = id;

    // Create Chart SVG element
    this.chart = d3.select(this.domid).append("svg:svg")
        .attr("class",  this.graph.cssClass)
        .attr("width",  this.graph.width)
        .attr("height", this.graph.height)
          .append("g")
            .attr("transform", "translate(0," + this.graph.height + ") scale(1,-1)");
    
    // height scale function
    var y_scaler = d3.scale.linear()
        .domain([this.graph.yAxis.min, this.graph.yAxis.max])
        .range([0, this.graph.height - this.graph.yAxis.gutter]);
    
    // height scale function
    var x_scaler = d3.scale.linear()
        .domain([this.graph.xAxis.min, this.graph.xAxis.max])
        .range([0, this.graph.width - this.graph.xAxis.gutter]);
    
    /*
    // Paint Chart
    this.chart.selectAll("g")
          .data(this.graph.data)
            .enter().append("line")
              .attr("x1", x1)
              .attr("y1", y_scaler)
              .attr("class", "line-color-one");
    
    */
    // Paint xaxis
    //var xaxis = new PlainXAxis(this.graph, this.chart);
    //xaxis.paint(this.graph.data.length * this.bar_width);
  };
};
