/**
 * Horizontal Bar Chart Class
 */
function HBar (css, w, h) {
  this.graph      = new Graph(css, w, h);
  this.bar_width  = 10;
  
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
    
    var bw = this.bar_width;
    var g  = this.graph.yAxis.gutter;
    
    // Paint Chart
    this.chart.selectAll("g")
          .data(this.graph.data)
            .enter().append("rect")
              .attr("y", this.graph.xAxis.gutter)
              .attr("x", function (d, i) {return i * bw + g})
              .attr("width", this.bar_width)
              .attr("height", y_scaler );
    
    // Paint xaxis
    var xaxis = new PlainXAxis(this.graph, this.chart);
    xaxis.paint(this.graph.data.length * this.bar_width);
  };
};
