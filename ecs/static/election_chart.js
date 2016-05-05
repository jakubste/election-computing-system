$(document).ready(function () {
    var $scatterChart = $("#election_chart");
    if ($scatterChart.length > 0) {
        $.get($scatterChart.data('url'), function (data) {
            var ctx = $scatterChart.get(0).getContext("2d");
            new Chart(ctx).Scatter(data['data'], {
                responsive: true,
                datasetFill: false,
                datasetStroke: false
            });
        });
    }
});
