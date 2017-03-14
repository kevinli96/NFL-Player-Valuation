 var yellow = '#A57706',
     red = '#D11C24',
     cyan = '#259286',
     tan = '#E7E0CB';

 var pic_height = 400, // height of svg image
     pic_width = 700, // width of svg image
     background_color = tan, // background color of image
     color_range = [yellow, red, cyan], // transitions of color
     bar_spacing = 0.2 // spacing between each bar

 var MIN_AV = -5
 var MAX_AV = 26

 var bardata = [] // empty array

 // pushing random data values onto bardata

 // MODIFY BELOW
 // such that bardata is filled with 32 values, each denoting
 // the counts corresponding to the AV at that index, with the domain
 // of the AVs going from -5 to 26
 // i.e. [15, 25, 30, ..., 20, 14]
 // there are 15 people with an AV of -5, 25 with an AV of -4
 // 20 with an AV of 25, 14 with an AV of 14

 for (var i = -5; i <= 26; i++) {
     bardata.push(Math.random() * 100);
 }
 console.log(bardata);

 // MODIFY ABOVE

 // Tooltip for hovering over bars to display value
 var tooltip = d3.select('body').append('div').attr("class", "tooltip")

 // setting margins for the svg
 var margin = {
     top: 30,
     right: 30,
     bottom: 40,
     left: 20
 }

 // height and width here denote the dimensions of the chart, 
 // as opposed to the dimensions of the svg (700 x 400), which is
 // of tan background color
 var height = pic_height - margin.top - margin.bottom,
     width = pic_width - margin.left - margin.right;

 // linear color scale - feel free to play around with the color_range 
 // array defined above
 var colors = d3.scaleLinear()
     .domain([0, bardata.length * .5, bardata.length])
     .range(color_range)

 // yscale goes from 0 to the maximum count of AV in bardata, ranging from
 // 0 to the chart height
 var yScale = d3.scaleLinear().domain([0, d3.max(bardata)]).range([0, height]);

 // xscale has a domain of the minimum AV value (-5) and the maximum AV value (26)
 var xScale = d3.scaleBand()
     .domain(d3.range(MIN_AV, MAX_AV + 1))
     .range([0, width])
     .paddingInner(bar_spacing)

 var svg = d3.select('#chart').append('svg')
     .style('background', background_color)
     .attr('width', width + margin.left + margin.right)
     .attr('height', height + margin.top + margin.bottom)
     .append('g')
     .attr('transform', 'translate(' + margin.left + ', ' + margin.top + ')')
     .selectAll('rect').data(bardata)
     .enter().append('rect')
     .style('fill', function(d, i) {
         return colors(i);
     })
     .attr('width', xScale.bandwidth())
     .attr('x', function(d, i) {
         return xScale(i - 5);
     })
     .attr('height', function(d) {
         return yScale(d);
     })
     .attr('y', function(d) {
         return height - yScale(d);
     })

 // ABOVE: height and y are sort of counterintuitive, because of SVG graphics
 // centering everything around a (0,0) coordinate at the top left of the SVG.

 var xAxis = d3.axisBottom(xScale).tickValues(d3.range(MIN_AV, MAX_AV + 1))

 var horizontal = d3.select('svg').append('g')
     .attr("class", "x axis")
     .attr('transform', 'translate(' + margin.left + ', ' + (height + margin.top) + ')')
     .call(xAxis)

// Applying mouseover functions to rectangles
 d3.selectAll("rect")
     .on("mouseover", mouseover)
     .on("mousemove", function(d, i) {
         mousemove(d)
     })
     .on("mouseout", mouseout);

 // TOOLTIP FUNCTIONS

 function mouseover() {
     tooltip.transition().style("opacity", 0.9);
 }

 function mousemove(data) {
     console.log(data);
     tooltip.text(data)
         .style("left", (d3.event.pageX - 34) + "px")
         .style("top", (d3.event.pageY - 12) + "px");
 }

 function mouseout() {
     tooltip.style("opacity", 0);
 }