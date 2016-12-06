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
        formatter: function(value) {
            var txt = $resultsSlider.data('results-descriptions').split(',')[value];
            return 'Current value: ' + txt;
        }
    });
    $resultsSlider.on('change', function (e) {
        if (e.value.newValue == 0)
            return;

        $result_pk = $resultsSlider.data('results-pks').split(',')[e.value.newValue - 1];

        var source;
        if ($result_pk === '') {
            source = $scatterChart.data('url')
        } else {
            source = '/elections/chart_data/result/' + $result_pk + '/'
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
