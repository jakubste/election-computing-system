from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from ecs.elections.algorithms.brute_force import BruteForce
from ecs.elections.algorithms.genetic import GeneticAlgorithm
from ecs.elections.election_generator import ElectionGenerator
from ecs.elections.forms import ResultForm
from ecs.elections.models import Election, BRUTE_ALGORITHM, GeneticAlgorithmSettings, GENETIC_ALGORITHM


def generate_election_name():
    NAME_PREFIX = 'Generated elections'
    NAME_SEPARATOR = ' - '

    election = Election.objects.filter(
        name__icontains=NAME_PREFIX
    ).order_by('name').last()

    if not election:
        return NAME_PREFIX + NAME_SEPARATOR + '1'
    else:
        num = int(election.name.split(NAME_SEPARATOR)[1])
        return NAME_PREFIX + NAME_SEPARATOR + str(num + 1)


def run():
    election_name = generate_election_name()
    voters_num = 50
    candidates_num = 50
    committee_size = 10
    p_parameter = 10

    election_name = str(raw_input(
        'Elections name    [' + election_name + ']: '
    )) or election_name
    voters_num = int(raw_input(
        'Voters number     [' + str(voters_num) + ']: '
    ) or voters_num)
    candidates_num = int(raw_input(
        'Candidates number [' + str(candidates_num) + ']: '
    ) or candidates_num)
    committee_size = int(raw_input(
        'Committee size    [' + str(committee_size) + ']: '
    ) or committee_size)
    p_parameter = int(raw_input(
        'P parameter       [' + str(p_parameter) + ']: '
    ) or p_parameter)

    brute = str(raw_input('Use Brute-force? [y/N] '))
    brute = True if brute == 'y' else False

    user = User.objects.filter(is_superuser=True).first()
    if not user:
        user = User.objects.create_superuser('admin', 'admin@admin.pl', 'admin')
        print 'Created superuser:', 'admin', 'admin@admin.pl', 'admin'

    election = Election.objects.create(user=user, name=election_name, committee_size=committee_size)

    generator = ElectionGenerator(
        election, candidates_num, voters_num,
        0, 0, 30,
        0, 0, 30,
    )
    generator.generate_elections()

    url = reverse('elections:election_details', args=(election.pk,))
    print 'Results avaiable on: ' + url

    if brute:
        result = ResultForm({
            'p_parameter': p_parameter,
            'algorithm': BRUTE_ALGORITHM
        }, election=election).save()
        algorithm = BruteForce(election, p_parameter)
        time, winners = algorithm.start()
        result.time = time
        for winner in winners:
            result.winners.add(winner)
        result.score = result.calculate_score()
        result.save()

    cycles = [20, 50, 100]
    crossing_probability = [50, 75, 100]
    mutation_probability = [10, 25, 50]

    for cycle in cycles:
        for cp in crossing_probability:
            for mp in mutation_probability:
                genetic_kwargs = {
                    'cycles': cycle,
                    'crossing_probability': cp,
                    'mutation_probability': mp,
                }
                result = ResultForm({
                    'p_parameter': p_parameter,
                    'algorithm': GENETIC_ALGORITHM
                }, election=election).save()
                GeneticAlgorithmSettings.objects.create(
                    result=result, **genetic_kwargs
                )
                algorithm = GeneticAlgorithm(election, p_parameter, **genetic_kwargs)
                time, winners = algorithm.start()
                result.time = time
                for winner in winners:
                    result.winners.add(winner)
                result.score = result.calculate_score()
                result.save()
