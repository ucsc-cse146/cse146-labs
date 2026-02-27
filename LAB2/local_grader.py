#!/usr/bin/env python3

"""
Do a local practice grading.
The score you recieve here is not an actual score,
but gives you an idea on how prepared you are to submit to the autograder.
"""

import math
import os
import sys

import numpy
import pandas

import autograder.assignment
import autograder.question

class Lab2(autograder.assignment.Assignment):
    def __init__(self, **kwargs):
        super().__init__(
            name = 'Practice Grading for Lab 2',
            questions = [
                T1A(50, "Task 1.A (get_stats)"),
                T3A(30, "Task 3.A (select_features_by_weight)"),
                T3B(20, "Task 3.B (test_subset_features)"),
            ], **kwargs)

class T1A(autograder.question.Question):
    def score_question(self, submission):
        # [(name, predictions, labels, expected), ...]
        test_cases = [
            (
                'single positive hit',
                [1],
                [1],
                {
                    'confusion_matrix': {'tp': 1, 'fn': 0, 'fp': 0, 'tn': 0},
                    'accuracy': 1.0, 'precision': 1.0, 'recall': 1.0, 'f1': 1.0,
                    'fnr': 0.0, 'fpr': numpy.nan,
                },
            ),
        ]

        actual_stats = submission.__all__.get_stats(test_cases[0][1], test_cases[0][2])
        self.check_not_implemented(actual_stats)

        self.full_credit()
        deduction = -(max(1, self.max_points // len(test_cases)))

        for (name, predictions, labels, expected_stats) in test_cases:
            actual_stats = submission.__all__.get_stats(predictions, labels)

            # Flatten out the stats (so the confusion matrix is at the base level).
            actual_stats = self._flatten_stats(actual_stats)
            expected_stats = self._flatten_stats(expected_stats)

            for (expected_key, expected_value) in expected_stats.items():
                if (expected_key not in actual_stats):
                    self.add_message("Test case '%s' is missing a key: '%s'." % (name, expected_key), add_score = deduction)
                    continue

                actual_value = actual_stats[expected_key]
                if (not self._check_equals(expected_value, actual_value)):
                    self.add_message("Test case '%s' is has an incorrect value for key '%s'. Expected: %0.2f, Got: %0.2f." % (name, expected_key, expected_value, actual_value), add_score = deduction)
                    continue

        self.cap_score()

    def _check_equals(self, a, b):
        if (math.isnan(a) and math.isnan(b)):
            return True

        return math.isclose(a, b, abs_tol = 0.01)

    def _flatten_stats(self, stats):
        new_stats = {}

        for (key, value) in stats.items():
            if (isinstance(value, dict)):
                for (inner_key, inner_value) in value.items():
                    new_stats[inner_key] = inner_value
            else:
                new_stats[key] = value

        return new_stats

class T3A(autograder.question.Question):
    def score_question(self, submission):
        # [(name, feature_names, weights, lower_than, higher_than, use_and, expected_names), ...]
        test_cases = [
            (
                'single positive hit',
                ['a'],
                [0.5],
                numpy.inf,
                -numpy.inf,
                True,
                ['a'],
            ),
        ]

        selected_names = submission.__all__.select_features_by_weight(*test_cases[0][1:-1])
        self.check_not_implemented(selected_names)

        self.full_credit()
        deduction = -(max(1, self.max_points // len(test_cases)))

        for (name, feature_names, weights, lower_than, higher_than, use_and, expected_names) in test_cases:
            selected_names = submission.__all__.select_features_by_weight(feature_names, weights, lower_than, higher_than, use_and)

            if (len(expected_names) != len(selected_names)):
                self.add_message("Test case '%s' does not have the expected number of selected columns." % (name), add_score = deduction)
                continue

            selected_names.sort()
            expected_names.sort()

            if (expected_names != selected_names):
                self.add_message("Test case '%s' does not have the expected selected columns." % (name), add_score = deduction)
                continue

        self.cap_score()

class T3B(autograder.question.Question):
    def score_question(self, submission):
        # Just test for shape and types.

        # First feature is useful, second is uninformative.
        features_train = pandas.DataFrame({
            'a': [1, 0, 1, 0],
            'b': [0.5, 0.5, 0.5, 0.5],
        })
        labels_train = pandas.Series([1, 0, 1, 0])
        features_test = pandas.DataFrame({
            'a': [1, 0],
            'b': [0.5, 0.5],
        })
        labels_test = pandas.Series([1, 0])
        selected_feature_names = ['a', 'b']

        weights, stats = submission.__all__.test_subset_features(features_train, labels_train, features_test, labels_test, selected_feature_names)
        self.check_not_implemented(weights)

        self.full_credit()

        expected_len = 2
        if (len(weights) != expected_len):
            self.fail("Unexpected number of weights. Expected: %d, Got: %d." % (expected_len, len(weights)))

        if (not isinstance(stats, dict)):
            self.fail("Returned stats is not a dict, found: %s." % (str(type(stats))))

        expected_len = 7
        if (len(stats) < expected_len):
            self.fail("Not enough stats/metrics returned. Expected: %d, Got: %d." % (expected_len, len(stats)))

        if (weights[0] < weights[1]):
            self.fail("Informative feature does not have a higher weight than a non-informative feature.")

def main(path):
    assignment = Lab2(input_dir = path)
    result = assignment.grade()

    print("***")
    print("This is NOT an actual grade, submit to the autograder for an actual grade.")
    print("***\n")

    print(result.report())

def _load_args(args):
    exe = args.pop(0)
    if (len(args) != 1 or ({'h', 'help'} & {arg.lower().strip().replace('-', '') for arg in args})):
        print("USAGE: python3 %s <submission path (.py or .ipynb)>" % (exe), file = sys.stderr)
        sys.exit(1)

    path = os.path.abspath(args.pop(0))

    return path

if (__name__ == '__main__'):
    main(_load_args(list(sys.argv)))
