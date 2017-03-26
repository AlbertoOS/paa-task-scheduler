#!/usr/bin/python
# -*- encoding: utf-8 -*-
import argparse


def greedy_selection(activities):
    if not activities:  # An empty string or list has false value
        print('Nenhuma atividade foi informada')
        return 0
    schedule = []
    schedule.append(activities[0])
    for activity in activities[1:]:  # Tasks except first one - if activities has only an element, the for loop doesn't execute
        begin, end = activity
        if (begin >= schedule[-1][1]):
            schedule.append(activity)

    return schedule


def find_solution(j, q, opt, activities):
    if j==-1:
        return list();
    if (1 + opt[q[j]] > opt[j-1]):
        selected = find_solution(q[j], q, opt, activities)
        selected.append(activities[j])
        return selected
    else:
        return find_solution(j - 1, q, opt, activities)


def compute_q(activities):
    # Maior indice dos elementos compatíveis com a tarefa i
    q = []
    for activity in activities:
        compatible_activities = [x for x in activities if x[1] <= activity[0]]
        if not compatible_activities:
            q.append(-1)  # Deve ser a primeira a para estar na seleção
        else:
            qj = max(compatible_activities, key=lambda x: activities.index(x))
            qj = activities.index(qj)
            q.append(qj)
    return q


def dynamic_selection(activities):
    opt = [-1] * (len(activities)-1)
    opt[0] = 0
    # Maior indice dos elementos compatíveis com a tarefa i
    q = compute_q(activities)
    for i in range(1, len(activities) - 1):
        opt[i] = max(opt[i - 1], opt[q[i]] + 1)
    selected_activities = find_solution(len(activities) - 1, q, opt, activities)
    return selected_activities


def recursive_compute(j,activities,q):
    if (j==-1):
        return [];
    add_activity = recursive_compute(q[j], activities, q)
    no_add_activity = recursive_compute(j - 1, activities, q)
    if len(add_activity) >= len(no_add_activity):
        add_activity.append(activities[j])
        return add_activity
    return no_add_activity


def backtracking_selection(activities):
    q = compute_q(activities)
    selected_activities = recursive_compute(len(activities) - 1, activities, q)
    return selected_activities


def main():
    parser = argparse.ArgumentParser(prog='paa-activity-selection', description='Parses a input file with activities')
    parser.add_argument('--inputfile', type=str, nargs='?', default='input.txt', metavar='I',
                        help='location of input file to be parsed (default: input.txt)')
    parser.add_argument('--method', type=str, nargs='?', default='all', metavar='M',
                        help='algorithm to be used to schedule activities (options: greedy, dynamic, backtracking)')
    args = parser.parse_args()
    print('Argumentos recebidos: ')
    print(args)
    inputfile = args.inputfile
    method = args.method

    with open(inputfile) as f:
        activities = [activity.split() for activity in f.read().splitlines()]
        #  print(activities) tarefas
        #  print(activities[0]) primeira tarefa
        #  print(activities[0][0]) inicio da primeira tarefa
        #  print(activities[0][1]) fim da primeira tarefa
    activities.sort(key=lambda activity: activity[1])

    def print_solution(schedule, method):
        print('\n{} tarefas foram escalonadas seguindo o método {}'.format(len(schedule), method))
        print(schedule)
        for index, activity in enumerate(schedule):
            print('Tarefa {} início: {} fim: {}'.format(index, activity[0], activity[1]))

    if method == 'backtracking':
        schedule = backtracking_selection(activities)
        method += ' (retroativo)'
        print_solution(schedule, method)
    elif method == 'dynamic':
        schedule = dynamic_selection(activities)
        method += ' (dinâmico)'
        print_solution(schedule, method)
    elif method == 'greedy':
        schedule = greedy_selection(activities)
        method += ' (guloso)'
        print_solution(schedule, method)
    else:
        schedules = [backtracking_selection(activities), dynamic_selection(activities), greedy_selection(activities)]
        methods = ['backtracking (retroativo)', 'dynamic (dinâmico)', 'greedy (guloso)']
        for i in range(len(methods)):
            print_solution(schedules[i], methods[i])


if __name__ == "__main__":
    main()
