/////////////////////////////////////
// Step 1: Write accessor functions //
//////////////////////////////////////

// Accessor functions for the four dimensions of our data
function x(d) {
    // Return player's cap hit
    return d.cap_hit
}
function y(d) {
    // Return player's av value
    return d.av_value
}
function color(d) {
    // Return player's position
    return d.position_id
}
function radius(d) {
  return 6
}
function key(d) {
    // Return player's name
    return d.name
}

//////////////
// Provided //
//////////////

// Chart dimensions
var margin = {top: 19.5, right: 19.5, bottom: 19.5, left: 39.5};
var width = 768 - margin.right;
var height = 400 - margin.top - margin.bottom;

// Various scales
var xScale = d3.scaleLinear().domain([0, 24200000]).range([0, width]),
    yScale = d3.scaleLinear().domain([-5, 26]).range([height, 0]),
    colorScale = d3.scaleOrdinal()
      .domain(["WR", "RB", "S", "CB", "DT", "DE", "T", "G", "TE", "OLB", "ILB", "QB", "LB", "C", "K", "P", "LS"])
      // .range(["#a6cee3", "#1f78b4", "#b2df8a", "#33a02c", "#fb9a99", "#e31a1c", "#fdbf6f", "#ff7f00", "#cab2d6", 
      //   "#6a3d9a", "#ffff99", "#b15928", "#8dd3c7", "#ffffb3", "#bebada", "#fb8072", "#80b1d3"]);
      .range(["#3957ff", "#d3fe14", "#c9080a", "#fec7f8", "#0b7b3e", "#0bf0e9", "#c203c8", 
        "#fd9b39", "#888593", "#906407", "#98ba7f", "#fe6794", "#10b0ff", "#ac7bff", "#fee7c0", "#964c63", "#1da49c"]);

// The x & y axes
var xAxis = d3.axisBottom(xScale).ticks(12, d3.format(",d")),
    yAxis = d3.axisLeft(yScale);

// Create the SVG container and set the origin
var svg = d3.select("#chart_av_salary").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

//////////////////////////////
// Step 2: Add x and y axes //
//////////////////////////////
svg.append("g")
    .attr("class", "axis")
    .attr("transform", "translate(0," + height + ")")
    .call(xAxis)

svg.append("g")
    .attr("class", "axis")
    .call(yAxis)

//////////////////////////////////////
// Step 3: Add axis and year labels //
//////////////////////////////////////
var xAxisLabel = svg.append("text")
                .attr("class", "label label-x-axis")
                .attr("transform",
                      "translate(" + (width - margin.right - 100) + " ," +
                                     (height - 10) + ")")
                .text("Cap Hit (Dollars)");

var yAxisLabel = svg.append("text")
                .attr("class", "label label-y-axis")
                .attr("transform",
                      "translate(" + margin.left/2 + " ," +
                                     50 + ") rotate(-90)")
                .text("AV Value");

var yearLabel = svg.append("text")
                .attr("class", "label year")
                .attr("transform",
                      "translate(" + (width - margin.right - 200) + " ," +
                                     (height - 30) + ")")
                .text("2005");

///////////////////////////
// Step 4: Load the data //
///////////////////////////

// Load the data.
d3.csv("av_salary_viz_test.csv", function(av_data) {

  function interpolateData(year) {
    data = [];
    for (i = 0; i < av_data.length; i++) {
      if (av_data[i].year == year) {
        data.push(av_data[i]);
      }
    }
    return data;
  }

  ///////////////////////
  // Step 4: Plot dots //
  ///////////////////////

  opacity_map = {"WR": 1, "RB": 1, "S": 1, "CB": 1, "DT": 1, "DE": 1, "T": 1, "G": 1, "TE": 1, "OLB": 1, "ILB": 1, "QB": 1, "LB": 1, "C": 1, "K": 1, "P": 1, "LS": 1};
  active_map =  {"WR": true, "RB": true, "S": true, "CB": true, "DT": true, "DE": true, "T": true, "G": true, "TE": true, "OLB": true, "ILB": true, "QB": true, "LB": true, "C": true, "K": true, "P": true, "LS": true};

  function add_dots(year) {

    svg.selectAll("circle").remove();

    var dot = svg.selectAll("circle")
              .data(interpolateData(year))
              .enter()
              .append("circle");

    dot
      .attr("cx", function(d) {return xScale(x(d));})
      .attr("cy", function(d) {return yScale(y(d));})
      .attr("r", function(d) {return radius(d);})
      .attr("class", function(d) {
        if (active_map[color(d)]) {
          return "dot " + color(d) + " active";
        } else {
          return "dot " + color(d);
        }
      })
      .style("fill", function(d) {return colorScale(color(d));})
      .style("opacity", function(d) {return opacity_map[color(d)]});

    dot.sort(function(a, b) {
      return radius(b) - radius(a);
    });

      // Add a title.
    dot.append("title").
        text(function(d) {return key(d)});

  }

  add_dots(2005);

  ///////////////////////////////////
  // Step 5: Add fluff and overlay //
  ///////////////////////////////////

  // Add an overlay for the year label.
  var box = yearLabel.node().getBBox();

  var overlay = svg.append("rect")
      .attr("x", box.x)
      .attr("y", box.y)
      .attr("transform",
            "translate(" + (width - margin.right - 200) + " ," +
                           (height - 30) + ")")
      .attr("width", box.width)
      .attr("height", box.height)
      .attr("class", "overlay")
      .on("mouseover", enableInteraction);

  ////////////////////////
  // Step 6: Transition //
  ////////////////////////

  // Start a transition that interpolates the data based on year.
  svg.transition()
      .duration(15000)
      .ease(d3.easeLinear)
      .tween("year", tweenYear)
      .on("end", enableInteraction);

  // After the transition finishes, you can mouseover to change the year.
  function enableInteraction() {
    // Create a year scale
    yearScale = d3.scaleLinear().domain([0, box.width]).range([2005, 2016]);

    // Cancel the current transition, if any.
    svg.transition().duration(0);

    // For the year overlay, add mouseover, mouseout, and mousemove events
    // that 1) toggle the active class on mouseover and out and 2)
    // change the displayed year on mousemove.

    overlay
        .on("mouseover", mouseover)
        .on("mouseout", mouseout)
        .on("mousemove", mousemove)
        .on("touchmove", mousemove);

    function mouseover() {
      yearLabel.classed("active", !yearLabel.classed("active"));
    }

    function mouseout() {
      yearLabel.classed("active", !yearLabel.classed("active"));
    }

    function mousemove() {
      var coords = d3.mouse(this);
      year = yearScale(coords[0]);
      yearLabel.text(Math.round(year));
      transitionYear(year);
    }
  }

  // Tweens the entire chart by first tweening the year, and then the data.
  // For the interpolated data, the dots and label are redrawn.
  function tweenYear() {
    var year = d3.interpolateNumber(2005, 2016);
    return function(t) {
      yearLabel.text(Math.round(year(t)));
      transitionYear((year(t)));
    };
  }

  function transitionYear(year) {
    add_dots(Math.round(year));
  }

  svg.append("g")
    .attr("class", "legendLinear")
    .attr("transform", "translate(20," + (height - 40) +")");

  var legendLinear = d3.legendColor()
    .shapeWidth(25)
    .shapeHeight(15)
    .orient('horizontal')
    .scale(colorScale)
    .on("cellclick", function(d){
      d3.selectAll("." + d).classed("active", !d3.selectAll("." + d).classed("active"));
      if (d3.selectAll("." + d).classed("active")) {
        d3.selectAll("." + d).style("opacity", 1);
        opacity_map[d] = 1;
        active_map[d] = true;
      } else {
        d3.selectAll("." + d).style("opacity", 0);
        opacity_map[d] = 0;
        active_map[d] = false;
      }
    });

  svg.select(".legendLinear")
    .call(legendLinear);

});


