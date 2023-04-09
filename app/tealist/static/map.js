<script>
  // Size ?
  var width = 960
  var height = 600

  // The svg
  var svg = d3.select("#tea_map")
    .append("svg")
    .attr("viewBox", `0 0 960 600`)

  // Map and projection
  var projection = d3.geoEckert3()
    .center([0, 20]) // GPS of location to zoom on
    .scale(width / 1.6 / Math.PI)
    .translate([width / 2, height / 2])

  d3.queue()
    .defer(d3.json, "{% static 'world-geo-small.json' %}") // World shape
    .defer(d3.csv, "{% static 'location_counts.csv' %}") // Position of circles
    .await(ready);

  function ready(error, dataGeo, data) {

    // Create a color scale
    var allContinent = d3.map(data, function (d) {
      return (d.country)
    }).keys()
    var color = d3.scaleOrdinal()
      .domain(allContinent)
      .range(d3.schemePaired);

    // Add a scale for bubble size
    var valueExtent = d3.extent(data, function (d) {
      return +d.n;
    })
    var size = d3.scaleSqrt()
      .domain(valueExtent) // What's in the data
      .range([15, 25]) // Size in pixel

    // Draw the map
    svg.append("g")
      .selectAll("path")
      .data(dataGeo.features)
      .enter()
      .append("path")
      .attr("fill", "#c5d3a0")
      .attr("d", d3.geoPath()
        .projection(projection)
      )
      .style("stroke", "#283618")
      .attr("stroke-width", 2)
      .style("opacity", 1)

    // create a tooltip
    var Tooltip = d3.select("#tea_map")
      .append("div")
      .attr("class", "map-tooltip  d-none d-sm-block")
      .style("opacity", 0)
      .style("background-color", "#1a240c")
      .style("border", "none")
      .style("border-width", "2px")
      .style("border-radius", "5px")
      .style("padding", ".75em")

    // Three function that change the tooltip when user hover / move / leave a cell
    var mouseover = function (d) {
      Tooltip.style("opacity", 1)
    }
    var mousemove = function (d) {

      Tooltip.html(d.country + ": " + d.n + " vendors")
        .style("left", (parseInt(d3.select(this).attr("cx")) + document.getElementById("tea_map").offsetLeft + 20) +
          "px")
        .style("top", (parseInt(d3.select(this).attr("cy")) + document.getElementById("tea_map").offsetTop) + "px")
    }
    var mouseleave = function (d) {
      Tooltip.style("opacity", 0)
    }

    // Add circles:

    svg
      .selectAll("myCircles")
      .data(data.sort(function (a, b) {
        return +b.n - +a.n
      }).filter(function (d, i) {
        return i < 1000
      }))
      .enter()
      .append("circle")
      .attr("cx", function (d) {
        return projection([+d.homelon, +d.homelat])[0]
      })
      .attr("cy", function (d) {
        return projection([+d.homelon, +d.homelat])[1]
      })
      .attr("r", function (d) {
        return size(+d.n)
      })
      .attr("class", "circle")
      .style("fill", "#1a240c")
      .attr("stroke", "#9dd02d")
      .attr("stroke-width", 2)
      .on("mouseover", mouseover)
      .on("mousemove", mousemove)
      .on("mouseleave", mouseleave)

    // Add markers

    svg.selectAll(".m")
      .data(data.sort(function (a, b) {
        return +b.n - +a.n
      }).filter(function (d, i) {
        return i < 1000
      }))
      .enter()
      .append("image")
      .attr('width', 20)
      .attr('height', 20)
      .attr("xlink:href", "{% static 'tea-marker.svg' %}")
      .attr("transform", (d) => {
        let p = projection([d.homelon, d.homelat]);
        return `translate(${p[0]-10}, ${p[1]-10})`;
      })
      .attr("cx", function (d) {
        return projection([+d.homelon, +d.homelat])[0]
      })
      .attr("cy", function (d) {
        return projection([+d.homelon, +d.homelat])[1]
      })
      .on("mouseover", mouseover)
      .on("mousemove", mousemove)
      .on("mouseleave", mouseleave)

  }
</script>