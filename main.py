import os
import re
import argparse
import Parse
from treys import Card, Evaluator
from itertools import combinations
from math import sqrt

CARDS = [
    '2c','2d','2h','2s',
    '3c','3d','3h','3s',
    '4c','4d','4h','4s',
    '5c','5d','5h','5s',
    '6c','6d','6h','6s',
    '7c','7d','7h','7s',
    '8c','8d','8h','8s',
    '9c','9d','9h','9s',
    'Tc','Td','Th','Ts',
    'Jc','Jd','Jh','Js',
    'Qc','Qd','Qh','Qs',
    'Kc','Kd','Kh','Ks',
    'Ac','Ad','Ah','As',
]

def print_results(title, label, expected, sample, std_dev=2, label_column_size=18, value_column_size=12, columns=5):
    full_width = label_column_size + value_column_size*columns + columns*3
    horizontal_divider = ('{:-^%d}' % full_width).format('')

    label_row = '{:^%d} | {:^%d} | {:^%d} | {:^%d} | {:^%d} | {:^%d}' % ((label_column_size,) + tuple(value_column_size for _ in range(5)))
    results_row = '{:^%d} | {:^%d} | {:^%d} | {:^%d} | {:^%d} | {:^%d}' % ((label_column_size,) + tuple(value_column_size for _ in range(5)))
    totals_row = '{:^%d} | {:^%df} | {:^%df} | {:^%df} | {:^%df} | {:^%d}' % ((label_column_size,) + tuple(value_column_size for _ in range(5)))
    column_value = '{:^%df}' % (value_column_size)

    sample_size = sum(sample.values())
    confidence_limit = ['68', '95', '99.7'][std_dev-1]

    print(horizontal_divider)
    print(('{:^%d}' % full_width).format('{}, {}% Confidence Limit, n={}'.format(title, confidence_limit, sample_size)))
    print(horizontal_divider)
    print(label_row.format(label, 'Expected', 'Sample', 'Lower', 'Upper', 'Size'))
    print(horizontal_divider)
    sums = [0 for _ in range(5)]
    for key in sample:
        sample_percentage = sample[key]/sample_size

        # Calculate standard error
        ## can't divide by zero
        if sample[key] != 0:
            standard_error = sqrt((expected[key] * (1-expected[key])) / sample[key])
            lower_percentage = expected[key] - std_dev*standard_error
            upper_percentage = expected[key] + std_dev*standard_error
        else:
            standard_error = None
            lower_percentage = None
            upper_percentage = None

        print(results_row.format(
                key,
                column_value.format(expected[key]),
                *(
                    # If value is None, do str(None), else print the float value
                    (column_value.format(x) if x != None else str(x)
                        for x in [sample_percentage, lower_percentage, upper_percentage])
                ),
                sample[key],
            )
        )
        sums[0] += expected[key]
        if standard_error:
            sums[1] += sample_percentage
            sums[2] += lower_percentage
            sums[3] += upper_percentage
        sums[4] += sample[key]
    print(horizontal_divider)
    print(totals_row.format('Sum', *(sum for sum in sums)))
    assert sample_size == sums[4] # Sanity check for sample size

def main():
    # Argparse
    argparser = argparse.ArgumentParser(description='Poker Hand Auditor')
    argparser.add_argument('path', type=str, help='Path to hand history directory')
    argparser.add_argument('--onlyme', action='store_true', help='Only count my hands')
    argparser.add_argument('--stdev', choices=[1,2,3], default=2, type=int,
                            help='Stdev for confidence limit, so 1 for 68%%, 2 for 95%%, and 3 for 99.7%%. Default=2')
    argparser.add_argument('--site', choices=['Bovada'], default='Bovada', type=str,
                            help='Which site\'s hand history is being parsed. Default=Bovada')
    args = argparser.parse_args()

    # Determine correct parser
    if args.site == 'Bovada':
        Parser = Parse.Bovada

    hand_probabilites = Parse.HAND_PROBABILITIES
    card_frequency = {x: 0 for x in CARDS}
    hand_frequency = {x: 0 for x in hand_probabilites.keys()}
    # Treys evaluator
    evaluator = Evaluator()

    for file in os.listdir(args.path):
        # Only open .txt files
        if not file.lower().endswith('.txt'):
            continue

        # Open file with parser
        b = Parser('{}\{}'.format(args.path, file))

        while True:
            # Get hole cards
            hole_cards = b.get_hole_cards(only_me=args.onlyme)
            if not hole_cards:
                break # EOF

            # Count card frequency of hole cards
            for c_1, c_2 in hole_cards:
                card_frequency[c_1] += 1
                card_frequency[c_2] += 1

            # Get board cards
            board = b.get_summary_board()
            if not board:
                continue

            # Count card frequency of board cards
            for c in board:
                card_frequency[c] += 1

            # Get all combinations of 5 card hands of hole cards with board
            # and count hand frequency
            for hc in hole_cards:
                for hand in combinations(list(hc)+board, 5):
                    # There doesn't seem to be support in Treys for
                    # evaluating 5 card hands, so split hand into 3 and 2
                    hand_treys_1 = [Card.new(c) for c in hand[:3]]
                    hand_treys_2 = [Card.new(c) for c in hand[3:5]]
                    # Evaluate hand for rank
                    hand_rank = evaluator.class_to_string(
                        evaluator.get_rank_class(
                            evaluator.evaluate(hand_treys_1, hand_treys_2)
                        )
                    ).lower()
                    hand_frequency[hand_rank] += 1

    print_results(
        'Distribution of Hands',
        'Hand',
        hand_probabilites,
        hand_frequency,
        std_dev=args.stdev
    )
    print_results(
        'Distribution of Cards',
        'Card',
        {x: 1/len(CARDS) for x in CARDS},
        card_frequency,
        std_dev=args.stdev
    )

if __name__ == '__main__':
    main()