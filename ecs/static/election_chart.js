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


    var $resultsSlider = $('#results-slider');
    $resultsSlider.slider({
        formatter: function (value) {
            return $resultsSlider.data('results-descriptions').split(',')[value];
        }
    });
    $resultsSlider.on('change', function (e) {
        var source;
        if (e.value.newValue == 0) {
            source = $scatterChart.data('url');
        } else {
            var $resultPk = $resultsSlider.data('results-pks').split(',')[e.value.newValue - 1];
            source = '/elections/chart_data/result/' + $resultPk + '/'
        }
        $.get(source, function (data) {
            var ctx = $scatterChart.get(0).getContext("2d");
            new Chart(ctx).Scatter(data['data'], {
                responsive: true,
                datasetFill: false,
                datasetStroke: false,
                animation: false
            });
        });

    })


});
