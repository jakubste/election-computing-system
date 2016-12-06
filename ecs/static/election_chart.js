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

    $(document).on('change', 'select[name=results_choice]', function (e) {
        $result_pk = $(e.target).find('option:selected').val();
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
    });

});
