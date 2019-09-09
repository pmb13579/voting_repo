function buildCharts(sample) {

  d3.json(`/samples/${sample}`).then(function(data) {

      console.log(data);

      var trace1 = {
        // x: ["0-10","10-20","20-30","30-40","40-50","50-60","60-70","70-80","80-90","90-100"],
        x: data.bins,
//        y: [9.9, 13.4, 11.7, 9.6, 6.5, 5.7, 3.2, 1.5, 0.6, 0.1],
        y: data.rep_values,
        name: "rep",
        marker: {
          color: 'rgba(255,0,0,1)'
        },
        type: "bar"
      };

      var trace2 = {
        x: data.bins,
        // y: [4.8, 8.6, 10.4, 9.6, 7.9, 10.7, 7.3, 4.2, 1.5, 0.6],
        y: data.dem_values,
        name: "dem",
        marker: {
          color: 'rgba(0,0,255,1)'
        },
        type: "bar"
      };

      data = [trace1, trace2];
     
      var layout = {
        title: "Votes by non-white percentage",
        height: 600,
        width: 800,
        barmode: "group"
      };
      
      Plotly.newPlot("pie", data, layout);

  });

}

function init() {

  // Grab a reference to the dropdown select element
  var selector = d3.select("#selDataset");

  // Use the list of sample names to populate the select options
  d3.json("/names").then((sampleNames) => {
    sampleNames.forEach((sample) => {
      selector
        .append("option")
        .text(sample)
        .property("value", sample);
    });

    // Use the first sample from the list to build the initial plots
    const firstSample = sampleNames[0];
    buildCharts(firstSample);
  });
}

function optionChanged(newSample) {
  // Fetch new data each time a new sample is selected
  buildCharts(newSample);
}

// Initialize the dashboard
init();
