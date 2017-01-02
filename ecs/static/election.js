function debounce(func, wait, immediate) {
	var timeout;
	return function() {
		var context = this, args = arguments;
		var later = function() {
			timeout = null;
			if (!immediate) func.apply(context, args);
		};
		var callNow = immediate && !timeout;
		clearTimeout(timeout);
		timeout = setTimeout(later, wait);
		if (callNow) func.apply(context, args);
	};
};

$(document).ready(function () {
    var $scatterChart = $("#election_chart");
    var scatterChart;
    if ($scatterChart.length > 0) {
        $.get($scatterChart.data('url'), function (data) {
            var ctx = $scatterChart.get(0).getContext("2d");
            scatterChart = new Chart.Scatter(ctx, {
                data: data['data'],
                options: {
                    responsive: true,
                    title: {
                        display: true,
                        text:  data['data']['title']
                    },
                    datasetFill: false,
                    datasetStroke: false,
                    showLines: false,
                    animation: false
                }
            });
        });
    }

    var $resultsSlider = $('#results-slider');
    if ($resultsSlider.length) {
        // http://stackoverflow.com/a/6299576/5349587
        var ticks = [];
        var i = 0;
        while (ticks.push(i++) <= $resultsSlider.data('slider-max')) {
        }

        $resultsSlider.slider({
            formatter: function (value) {
                return $resultsSlider.data('results-descriptions').split(',')[value];
            },
            ticks: ticks,
            ticks_labels: $resultsSlider.data('results-p-params').split(',')
        });

        var updateScatter = function () {
            var source;
            var $inputResultsSlider = $('input#results-slider');
            if ($inputResultsSlider.val() == 0) {
                source = $scatterChart.data('url');
            } else {
                var $resultPk = $resultsSlider.data('results-pks').toString().split(',')[$inputResultsSlider.val() - 1];
                source = '/elections/chart_data/result/' + $resultPk + '/'
            }

            $.get(source, function (data) {
                if (scatterChart != null) {
                    scatterChart.destroy();
                }
                var ctx = $scatterChart.get(0).getContext("2d");
                scatterChart = new Chart.Scatter(ctx, {
                    data: data['data'],
                    options: {
                        responsive: true,
                        title: {
                            display: true,
                            text: data['data']['title']
                        },
                        datasetFill: false,
                        datasetStroke: false,
                        showLines : false,
                        animation: false,
                        reverse: true
                    }

                });
            });
        };

        $resultsSlider.on('change', debounce(updateScatter, 150));
    }

    var $algorithm_selection = $('select#id_algorithm');
    if ($algorithm_selection.length) {
        var toggleVisibilityGeneticForm = function () {
            var $geneticForm = $('#genetic_form');
            var $algorithm_selection = $('select#id_algorithm');
            if ($algorithm_selection.val() == 'g') {
                $geneticForm.show();
            } else {
                $geneticForm.hide();
            }
        };
        $algorithm_selection.on('change', toggleVisibilityGeneticForm);
        toggleVisibilityGeneticForm();
    }

    var $algorithms_chart = $("#algorithms_chart");
    $.get($algorithms_chart.data('url'), function (data) {
        if($algorithms_chart.length == 0)
            return;
        var ctx = $algorithms_chart.get(0).getContext("2d");
        new Chart(ctx, {
            type: 'bar',
            data: data['data'],
            options: {
                showLines: true,
                spanGaps: true,
                responsive: true,
                title:{
                    display:true,
                    text:'Time measured for given algorithm and p'
                },
                scales: {
                    xAxes: [{
                        display: true,
                        scaleLabel: {
                            display: true,
                            labelString: 'p'
                        }
                    }],
                    yAxes: [{
                        display: true,
                        scaleLabel: {
                            display: true,
                            labelString: 'time [s]'
                        },
                        id: 'time',
                        position: 'left',
                        ticks: {
                            min: 0
                        }
                    },
                    {
                        display: true,
                        scaleLabel: {
                            display: true,
                            labelString: 'score'
                        },
                        id: 'score',
                        position: 'right',
                        ticks: {
                            min: 0
                        }
                    }]
                }
            }
        });
    })
});
