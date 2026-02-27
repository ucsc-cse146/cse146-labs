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
import sklearn.linear_model

import autograder.assignment
import autograder.question

class Lab3(autograder.assignment.Assignment):
    def __init__(self, **kwargs):
        super().__init__(
            name = 'Lab 3',
            questions = [
                T1A(1, "Task 1.A (train_test_split)"),
                T1B(1, "Task 1.B (remove_protected_attributes)"),
                T1C(1, "Task 1.C (get_group_ids)"),
                T2A(1, "Task 2.A (train_and_predict)"),
                T3A(1, "Task 3.A (get_stats)"),
                T3B(1, "Task 3.B (equalized_odds)"),
                T3C(1, "Task 3.C (demographic_parity)"),
            ], **kwargs)

class T1A(autograder.question.Question):
    def score_question(self, submission):
        # [(name, data, label column, train_ratio, expected_x_train, expected_x_test, expected_y_train, expected_y_test), ...]
        test_cases = [
            (
                'two columns, first is label',
                {'a': [1, 2, 3, 4], 'b': [5, 6, 7, 8]},
                'a', 0.5,
                {'b': [5, 6]}, {'b': [7, 8]},
                [1, 2], [3, 4],
            ),
        ]

        x_train, _, _, _ = submission.__all__.train_test_split(pandas.DataFrame(test_cases[0][1]), test_cases[0][2], test_cases[0][3])
        self.check_not_implemented(x_train)

        self.full_credit()
        deduction = -(max(1, self.max_points // len(test_cases)))

        for (name, data, label_column_name, train_ratio, expected_x_train, expected_x_test, expected_y_train, expected_y_test) in test_cases:
            data = pandas.DataFrame(data)

            expected_x_train = pandas.DataFrame(expected_x_train)
            expected_x_test = pandas.DataFrame(expected_x_test)

            expected_y_train = pandas.Series(expected_y_train)
            expected_y_test = pandas.Series(expected_y_test)

            actual_x_train, actual_x_test, actual_y_train, actual_y_test = submission.__all__.train_test_split(data, label_column_name, train_ratio = train_ratio)

            comparisons = [
                ('train features', expected_x_train, actual_x_train),
                ('test features', expected_x_test, actual_x_test),
                ('train labels', expected_y_train, actual_y_train),
                ('test labels', expected_y_test, actual_y_test),
            ]

            for (comparison_name, expected, actual) in comparisons:
                if (not _pandas_contents_equals(expected, actual)):
                    self.add_message("Failed test case '%s': %s are not as expected." % (name, comparison_name), add_score = deduction)

        self.cap_score()

class T1B(autograder.question.Question):
    def score_question(self, submission):
        # [(name, data, protected_frame, expected), ...]
        test_cases = [
            (
                'basic',
                {'a': [1, 2, 3], 'b': [4, 5, 6], 'c': [7, 8, 9]},
                {'a': [0], 'b': [1], 'c': [2]},
                {'a': [1, 2, 3], 'c': [7, 8, 9]},
            ),
        ]

        result = submission.__all__.remove_protected_attributes(pandas.DataFrame(test_cases[0][1]), pandas.DataFrame(test_cases[0][2]))
        self.check_not_implemented(result)

        self.full_credit()
        deduction = -(max(1, self.max_points // len(test_cases)))

        for (name, data, protected_data, expected) in test_cases:
            data = pandas.DataFrame(data)
            protected_data = pandas.DataFrame(protected_data)
            expected = pandas.DataFrame(expected)

            actual = submission.__all__.remove_protected_attributes(data, protected_data)
            if (not _pandas_contents_equals(expected, actual)):
                self.add_message("Failed test case '%s': result is not as expected." % (name), add_score = deduction)

        self.cap_score()

class T1C(autograder.question.Question):
    def score_question(self, submission):
        # [(name, data, group_column_name, group_threshold, expected), ...]
        test_cases = [
            (
                'ascending values',
                {'a': [1, 2, 3, 4], 'b': [9, 8, 7, 6], 'c': [40, 10, 50, -20]},
                'a', 2.5,
                [0, 0, 1, 1],
            ),
        ]

        result = submission.__all__.get_group_ids(pandas.DataFrame(test_cases[0][1]), test_cases[0][2], test_cases[0][3])
        self.check_not_implemented(result)

        self.full_credit()
        deduction = -(max(1, self.max_points // len(test_cases)))

        for (name, data, group_column_name, group_threshold, expected) in test_cases:
            data = pandas.DataFrame(data)

            actual = submission.__all__.get_group_ids(data, group_column_name, group_threshold)
            if (expected != actual):
                self.add_message("Failed test case '%s': result is not as expected." % (name), add_score = deduction)

        self.cap_score()

class T2A(autograder.question.Question):
    def score_question(self, submission):
        features = pandas.DataFrame({
            'a': [0, 1, 0, 1, 0, 1],
            'b': [1, 0, 1, 0, 1, 0],
        })

        labels = pandas.Series([True, False, True, False, True, False])

        predictions, classifier = submission.__all__.train_and_predict(features, labels, features)
        self.check_not_implemented(predictions)

        if (not isinstance(classifier, sklearn.linear_model.LogisticRegression)):
            self.fail("Classifier is not a sklearn.linear_model.LogisticRegression.")

        score = classifier.score(features, labels)
        if (not math.isclose(score, 1.0)):
            self.fail("Classifier was not trained properly (it could not score perfectly on idea data).")

        self.full_credit()

class T3A(autograder.question.Question):
    def score_question(self, submission):
        # [(name, predictions, labels, threshold, expected), ...]
        test_cases = [
            (
                'single positive hit',
                [1],
                [1],
                0.5,
                {
                    'f1': 1.0,
                    'fpr': numpy.nan,
                    'tpr': 1.0,
                    'pr': 1.0,
                },
            ),
        ]

        actual_stats = submission.__all__.get_stats(test_cases[0][1], test_cases[0][2], test_cases[0][3])
        self.check_not_implemented(actual_stats)

        self.full_credit()
        deduction = -(max(1, self.max_points // len(test_cases)))

        for (name, predictions, labels, threshold, expected_stats) in test_cases:
            actual_stats = submission.__all__.get_stats(predictions, labels, threshold)

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

class T3B(autograder.question.Question):
    def score_question(self, submission):
        # [(name, a_stats, b_stats, expected), ...]
        test_cases = [
            (
                'medium bias',
                {'fpr': 0.50, 'tpr': 0.50, 'f1': 100, 'pr': 1000},
                {'fpr': 0.25, 'tpr': 0.25, 'f1': 200, 'pr': 2000},
                0.50,
            ),
        ]

        result = submission.__all__.equalized_odds(test_cases[0][1], test_cases[0][2])
        self.check_not_implemented(result)

        self.full_credit()
        deduction = -(max(1, self.max_points // len(test_cases)))

        for (name, a_stats, b_stats, expected) in test_cases:
            actual = submission.__all__.equalized_odds(a_stats, b_stats)
            if (not math.isclose(expected, actual, abs_tol = 0.01)):
                self.add_message("Test case '%s' is has an incorrect value. Expected: %0.2f, Got: %0.2f." % (name, expected, actual), add_score = deduction)

        self.cap_score()

class T3C(autograder.question.Question):
    def score_question(self, submission):
        # [(name, a_stats, b_stats, expected), ...]
        test_cases = [
            (
                'medium bias',
                {'pr': 0.50, 'fpr': 10000, 'tpr': 1000, 'f1': 100},
                {'pr': 0.25, 'fpr': 20000, 'tpr': 2000, 'f1': 200},
                0.25,
            ),
        ]

        result = submission.__all__.demographic_parity(test_cases[0][1], test_cases[0][2])
        self.check_not_implemented(result)

        self.full_credit()
        deduction = -(max(1, self.max_points // len(test_cases)))

        for (name, a_stats, b_stats, expected) in test_cases:
            actual = submission.__all__.demographic_parity(a_stats, b_stats)
            if (not math.isclose(expected, actual, abs_tol = 0.01)):
                self.add_message("Test case '%s' is has an incorrect value. Expected: %0.2f, Got: %0.2f." % (name, expected, actual), add_score = deduction)

        self.cap_score()

def _pandas_contents_equals(a, b, reset_index = True):
    if ((a is None) and (b is None)):
        return True

    if ((a is None) or (b is None)):
        return False

    if (a.empty and b.empty):
        return True

    if (a.empty or b.empty):
        return False

    if ((len(a) == 0) and (len(b) == 0)):
        return True

    if ((len(a) == 0) or (len(b) == 0)):
        return False

    if (reset_index):
        a = a.reset_index(drop = True)
        b = b.reset_index(drop = True)

    return a.equals(b)

def main(path):
    assignment = Lab3(input_dir = path)
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
