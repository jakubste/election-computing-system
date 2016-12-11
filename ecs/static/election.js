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
    if ($resultsSlider.length) {
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
                var ctx = $scatterChart.get(0).getContext("2d");
                new Chart(ctx).Scatter(data['data'], {
                    responsive: true,
                    datasetFill: false,
                    datasetStroke: false,
                    animation: false
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
});
