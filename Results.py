from scipy.stats import chisquare, kstest
from math import sqrt

class Results:
    DEFAULT_COLUMN_SIZE=15

    def __init__(self, label_column_size=DEFAULT_COLUMN_SIZE, value_column_size=DEFAULT_COLUMN_SIZE, columns=6, summary_only=False):
        self._summary_only = summary_only
        self.set_label_column_size(label_column_size)
        self.set_value_column_size(value_column_size)
        self.set_full_width(6)

    # Set sizes and formatting values based on size
    def set_label_column_size(self, size):
        self._label_column_size = size
        self._label_column = '{:^%d}|' % self._label_column_size
    def set_value_column_size(self, size):
        # Various column formats
        self._value_column_size = size
        self._value_column = '{:^%d}|' % self._value_column_size
        self._float_value_column = '{:^%df}|' % self._value_column_size
        self._float_value = '{:^%df}' % self._value_column_size
    def set_full_width(self, columns):
        # Various column formats
        self._full_width = self._label_column_size + self._value_column_size*columns + columns
        self._horizontal_divider = ('{:-^%d}' % self._full_width).format('')
        self._value_span_fullwidth = '{:^%d}|' % self._full_width
        self._float_value_span_halfwidth = '{:^%df}' % (self._full_width // 2)
        self._value_column_span_halfwidth = '{:^%d}|' % (self._full_width // 2)

        # Row formats
        self._results_row = self._label_column + self._value_column*columns
        self._halfwidth_value_span_row = self._value_column_span_halfwidth*2
        self._totals_row = self._label_column + self._float_value_column + self._value_column + self._float_value_column*(columns-3) + self._value_column

    # Printing rows
    def _print_row(self, s, divider=False, is_summary=False):
        if not self._summary_only or self._summary_only and is_summary:
            print(s)
            if divider:
                self.print_horizontal_divider(is_summary=is_summary)
    def print_results_row(self, *argv, divider=False, is_summary=False):
        self._print_row(self._results_row.format(*argv), divider, is_summary)
    def print_halfwidth_value_span_row(self, *argv, divider=False, is_summary=False):
        self._print_row(self._halfwidth_value_span_row.format(*argv), divider, is_summary)
    def print_halfwidth_float_span_row(self, label, *argv, divider=False, is_summary=False):
        self.print_halfwidth_value_span_row(
            label,
            self._format_if_valid(
                self._float_value_span_halfwidth,
                *argv
            ),
            divider=divider,
        )
    def print_fullwidth_value_span_row(self, *argv, divider=False, is_summary=False):
        self._print_row(self._value_span_fullwidth.format(*argv), divider, is_summary)
    # Totals row used in calculate_and_print_results
    def print_totals_row(self, *argv, divider=False, is_summary=False):
        self._print_row(self._totals_row.format(*argv), divider, is_summary)

    def _format_if_valid(self, format_str, val, append_on_none=''):
        return format_str.format(val) if val != None else str(val)+append_on_none
    def print_horizontal_divider(self, is_summary=False):
        if not self._summary_only or self._summary_only and is_summary:
            print(self._horizontal_divider)
    def print_string_with_divider(self, s, is_summary=False):
        if not self._summary_only or self._summary_only and is_summary:
            print(s)
            self.print_horizontal_divider(is_summary=is_summary)

    # Print table of results
    ## title: str, title of the table
    ## label: str, label of the first column
    ## expected: dict, expected values
    ## sample: dict, sampled values
    ## std_dev: int 1,2,3, std_dev for use in confidence limit
    ## label_column_size: int, width of first column
    ## value_column_size: int, width of other columns
    ## is_normal: bool, is normally distributed, whether to calculate confidence intervals
    ## Returns float, chi_square_pvalue
    def calculate_and_print_results(self, title, label, expected, sample, summary=None,
                                    test_results=None, std_dev=2, is_normal=True, pvalues=None,
                                    no_output=False):
        if no_output:
            prev_summary_only_val = self._summary_only
            self._summary_only = True

        columns = 6 if is_normal else 4
        self.set_full_width(columns)

        sample_size = sum(sample.values())

        # Print title and column headers
        self.print_string_with_divider('')
        if is_normal:
            confidence_limit = ['68', '95', '99.7'][std_dev-1]
            table_title = '{}, {}% Confidence Level, n={}'.format(title, confidence_limit, sample_size)
            column_name_args = (label, 'Expected', 'Expected Size','Sample', 'Lower', 'Upper', 'Sample Size')
            # Track proportion values as list of tuples (sample,lower,upper)
            proportions = []
        else:
            table_title = '{}, n={}'.format(title, sample_size)
            column_name_args = (label, 'Expected', 'Expected Size','Sample', 'Sample Size')
        self.print_fullwidth_value_span_row(table_title, divider=True)
        self.print_results_row(*column_name_args, divider=True)

        totals = [0 for _ in range(columns)]
        expected_sizes = []

        # Print column values
        for key in sample:
            sample_percentage = sample[key]/sample_size
            expected_size = round(expected[key]*sample_size)
            expected_sizes.append(expected_size)

            # Print row of values
            if is_normal:
                # Calculate standard error
                ## can't divide by zero
                if sample[key] != 0:
                    standard_error = sqrt((expected[key] * (1-expected[key])) / sample[key])
                    lower_percentage = expected[key] - std_dev*standard_error
                    upper_percentage = expected[key] + std_dev*standard_error
                    proportions.append((sample_percentage, lower_percentage, upper_percentage))
                else:
                    standard_error = None
                    lower_percentage = None
                    upper_percentage = None

                self.print_results_row(
                    key, # Label
                    self._format_if_valid(self._float_value, expected[key]), # Expected proportion
                    expected_size, # Expected size
                    self._format_if_valid(self._float_value, sample_percentage), # Sample proportion
                    self._format_if_valid(self._float_value, lower_percentage), # Upper confidence limit
                    self._format_if_valid(self._float_value, upper_percentage), # Lower confidence limit
                    sample[key], # Sample size
                )
            else:
                self.print_results_row(
                    key, # Label
                    self._format_if_valid(self._float_value, expected[key]), # Expected proportion
                    expected_size, # Expected size
                    self._format_if_valid(self._float_value, sample_percentage), # Sample proportion
                    sample[key], # Sample size
                )


            # Count totals
            totals[0] += expected[key]
            if is_normal:
                totals[1] += expected_size
                if standard_error:
                    totals[2] += sample_percentage
                    totals[3] += lower_percentage
                    totals[4] += upper_percentage
                totals[5] += sample[key]
            else:
                totals[1] += expected_size
                totals[2] += sample_percentage
                totals[3] += sample[key]
        self.print_horizontal_divider()
        self.print_totals_row('Total', *(total for total in totals), divider=True)

        # Find and print chi-square and Kolmogorov-Smirnov values
        sample_values = list(sample.values())
        # Remove expected sizes of 0
        zero_in_expected_sizes = 0 in expected_sizes
        if zero_in_expected_sizes:
            for adjust, index in enumerate([i for i in range(len(expected_sizes)) if expected_sizes[i] == 0]):
                del sample_values[index-adjust]
                del expected_sizes[index-adjust]
        chi_square, chi_square_pvalue = chisquare(sample_values, f_exp=expected_sizes)

        self.print_fullwidth_value_span_row(
            'Chi-Square Goodness of Fit Test{}'.format(
                ' (Excluding expected value(s)==0)' if zero_in_expected_sizes else ''
            ),
            divider=True
        )
        self.print_halfwidth_float_span_row('Chi-square', chi_square, divider=False)
        self.print_halfwidth_float_span_row('Chi-square p-value', chi_square_pvalue, divider=True)

        assert sample_size == totals[5 if is_normal else 3] # Sanity check for sample size

        # Write summary of results
        if summary != None and test_results != None:
            summary.append(('{}, n={}'.format(title, sample_size), []))
            if is_normal:
                test_results.append(all([l < s < u for s,l,u in proportions]))
                summary[-1][1].append((
                    'Sample in {}% confidence interval'.format(confidence_limit),
                    'PASS' if test_results[-1] else 'FAIL',
                ))
            if chi_square_pvalue != None:
                test_results.append(chi_square_pvalue > 0.05)
                summary[-1][1].append((
                    'Chi-square p-value > 0.05',
                    'PASS' if test_results[-1] else 'FAIL',
                ))

        if pvalues != None:
            pvalues.append((sample_size, chi_square_pvalue))

        if no_output:
            self._summary_only = prev_summary_only_val

    # Print kstest table
    def print_kstest_table(self, chi_square_pvalues, title, summary=None,
                           test_results=None, column_size=30):
        initial_sizes = (self._label_column_size, self._value_column_size, self._full_width)
        sample_size = sum([x[0] for x in chi_square_pvalues])
        self.set_label_column_size(column_size)
        self.set_value_column_size(column_size)
        self.set_full_width(1)

        self.print_horizontal_divider()
        self.print_fullwidth_value_span_row(
            f'{title}, n={sample_size}, bins={len(chi_square_pvalues)}',
            divider=True
        )
        self.print_halfwidth_value_span_row('Bin', 'p-value', divider=True)
        for i, t in enumerate(chi_square_pvalues):
            self.print_halfwidth_float_span_row(str(i), t[1], divider=False)
        self.print_horizontal_divider()

        self.print_fullwidth_value_span_row('Kolmogorov-Smirnov uniformity test of Chi-square p-values', divider=True)
        ks, ks_pvalue = kstest([p[1] for p in chi_square_pvalues], 'uniform')
        self.print_halfwidth_float_span_row('KS', ks, divider=False)
        self.print_halfwidth_float_span_row('p-value', ks_pvalue, divider=True)

        self.set_label_column_size(initial_sizes[0])
        self.set_value_column_size(initial_sizes[1])
        self.set_full_width(initial_sizes[2])

        # Add to last summary test results
        if summary != None and test_results != None:
            # Assume
            test_results.append(ks_pvalue > 0.05)
            summary[-1][1].append((
                'KS uniformity p-value > 0.05',
                'PASS' if test_results[-1] else 'FAIL',
            ))

    # Print summary
    ## summary: list of pair of strs
    ## test_results: list of bool
    def print_summary(self, summary, test_results):
        self.set_full_width(4)

        self.print_string_with_divider('', is_summary=True)
        self.print_fullwidth_value_span_row('SUMMARY', divider=True, is_summary=True)
        for title,details in summary:
            self.print_fullwidth_value_span_row(title, divider=True, is_summary=True)
            self.print_halfwidth_value_span_row('Test', 'Result', divider=True, is_summary=True)
            for test, result in details:
                self.print_halfwidth_value_span_row(test, result, is_summary=True)
            self.print_horizontal_divider(is_summary=True)
        self.print_fullwidth_value_span_row(
            'Passing Tests: {}/{}'.format(test_results.count(True), len(test_results)),
            divider=True,
            is_summary=True,
        )
