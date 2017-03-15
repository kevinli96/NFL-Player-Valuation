 var yellow = '#A57706',
     red = '#D11C24',
     cyan = '#259286',
     tan = '#E7E0CB';

 var pic_height = 400, // height of svg image
     pic_width = 700, // width of svg image
     background_color = tan, // background color of image
     color_range = [yellow, cyan, red], // transitions of color
     bar_spacing = 0.2 // spacing between each bar

 var MIN_AV = -5
 var MAX_AV = 26

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

 function drawChart(chartId, position) {
     var bardata = [];
     d3.tsv('data/' + position
      + '_AV_counts.tsv', function(data) {
         for (key in data) {
             bardata.push(parseInt(data[key].value))
         }
         drawHistogram(chartId, bardata, position);
     })
 }


 function drawHistogram(chartId, bardata, position) {
     bardata = bardata.slice(0, 32)

     var tooltip = d3.select('body').append('div').attr("class", "tooltip")
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
     var svg = d3.select('#' + chartId).append('svg')
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


     d3.select('svg').append("text")
         .attr("x", (width / 2))
         .attr("y", 50)
         .attr("text-anchor", "middle")
         .style("font-size", "24px")
         .text(position + " AV Counts");

     // ABOVE: height and y are sort of counterintuitive, because of SVG graphics
     // centering everything around a (0,0) coordinate at the top left of the SVG.

     var xAxis = d3.axisBottom(xScale).tickValues(d3.range(MIN_AV, MAX_AV + 1))

     var horizontal = d3.select('svg').append('g')
         .attr("class", "x axis")
         .attr('transform', 'translate(' + margin.left + ', ' + (height + margin.top) + ')')
         .call(xAxis)

     // Applying mouseover functions to rectangles
     d3.selectAll("rect")
         .on("mouseover", function(d) {
             tooltip.transition().style("opacity", 0.9);
         })
         .on("mousemove", function(d, i) {
             tooltip.text(d)
                 .style("left", (d3.event.pageX - 34) + "px")
                 .style("top", (d3.event.pageY - 12) + "px");
         })
         .on("mouseout", function(d) {
             tooltip.style("opacity", 0);
         });
 }
 
 drawChart("chart", "QB")