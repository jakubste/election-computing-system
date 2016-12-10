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
    // http://stackoverflow.com/a/6299576/5349587
    var ticks = [];
    var i = 0;
    while (ticks.push(i++) <= $resultsSlider.data('slider-max')) {}

    $resultsSlider.slider({
        formatter: function (value) {
            return $resultsSlider.data('results-descriptions').split(',')[value];
        },
        ticks: ticks,
        ticks_labels: $resultsSlider.data('results-p-params').split(',')
    });
    $resultsSlider.on('change', function (e) {
        var source;
        if (e.value.newValue == 0) {
            source = $scatterChart.data('url');
        } else {
            var $resultPk = $resultsSlider.data('results-pks').toString().split(',')[e.value.newValue - 1];
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
    });

    var $algorithm_selection = $('select#id_algorithm');
    $algorithm_selection.on('change', function (e) {
        var $geneticForm = $('#genetic_form');
        if (e.target.value == 'g') {
            $geneticForm.show();
        } else {
            $geneticForm.hide();
        }
    });

});
