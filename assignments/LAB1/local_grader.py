#!/usr/bin/env python3

"""
Do a local practice grading.
The score you recieve here is not an actual score,
but gives you an idea on how prepared you are to submit to the autograder.
"""

import math
import os
import sys

import pandas
import sklearn.linear_model
import sklearn.tree

import autograder.assignment
import autograder.question

class Lab1(autograder.assignment.Assignment):
    def __init__(self, **kwargs):
        super().__init__(
            name = 'Practice Grading for Lab 1',
            questions = [
                T2A(1, "Task 2.A (slice_labels)"),
                T2B(1, "Task 2.B (split_data)"),
                T3A(1, "Task 3.A (get_trained_lr)"),
                T3B(1, "Task 3.B (get_trained_dt)"),
                T4A(1, "Task 4.A (get_train_size_scores)"),
                T4B(1, "Task 4.B (get_dt_max_depth_scores)"),
                T5A(1, "Task 5.A (split_on_column)"),
                T5B(1, "Task 5.B (compute_disparity)"),
                T5C(1, "Task 5.C (compute_confusion_disparity)"),
            ], **kwargs)

class T2A(autograder.question.Question):
    def score_question(self, submission):
        # [(name, data, label column, expected_x, expected_y), ...]
        test_cases = [
            ('two columns, first is label', {'a': [1, 2, 3], 'b': [4, 5, 6]}, 'a', {'b': [4, 5, 6]}, [1, 2, 3]),
        ]

        x, y = submission.__all__.slice_labels(pandas.DataFrame(test_cases[0][1]), test_cases[0][2])
        self.check_not_implemented(x)

        self.full_credit()
        deduction = -(max(1, self.max_points // len(test_cases)))

        for (name, data, label_column_name, expected_x, expected_y) in test_cases:
            data = pandas.DataFrame(data)
            expected_x = pandas.DataFrame(expected_x)
            expected_y = pandas.Series(expected_y)

            actual_x, actual_y = submission.__all__.slice_labels(data, label_column_name)

            if (not _pandas_contents_equals(expected_x, actual_x)):
                self.add_message("Failed test case '%s': features are not as expected." % (name), add_score = deduction)
                continue

            if (not _pandas_contents_equals(expected_y, actual_y)):
                self.add_message("Failed test case '%s': labels are not as expected." % (name), add_score = deduction)
                continue

        self.cap_score()

class T2B(autograder.question.Question):
    def score_question(self, submission):
        base_features = pandas.DataFrame({
            'a': [1, 2, 3, 4, 5, 6],
            'b': ['a', 'b', 'c', 'd', 'e', 'f'],
        })

        base_labels = pandas.Series([True, False, True, False, True, False])

        features_train, features_test, labels_train, labels_test = submission.__all__.split_data(base_features, base_labels, 3)
        self.check_not_implemented(features_train)

        test_cases = [
            (3, 'half train, half test'),
        ]

        self.full_credit()
        deduction = -(max(1, self.max_points // len(test_cases)))

        for (train_size, name) in test_cases:
            features_train, features_test, labels_train, labels_test = submission.__all__.split_data(base_features, base_labels, train_size)

            split_cases = [
                ('train', features_train, labels_train, train_size),
                ('test', features_test, labels_test, len(base_labels) - train_size),
            ]

            for (split, features, labels, expected_size) in split_cases:
                if (len(features) != len(labels)):
                    self.add_message("Test case '%s': Number of %s features and labels do not match." % (name, split), add_score = deduction)
                    continue

                if (len(features) != expected_size):
                    self.add_message("Test case '%s': Number of %s features/labels not as expected." % (name, split), add_score = deduction)
                    continue

        self.cap_score()

class T3A(autograder.question.Question):
    def score_question(self, submission):
        features = pandas.DataFrame({
            'a': [0, 1, 0, 1, 0, 1],
            'b': [1, 0, 1, 0, 1, 0],
        })

        labels = pandas.Series([True, False, True, False, True, False])

        classifier = submission.__all__.get_trained_lr(features, labels)
        self.check_not_implemented(classifier)

        if (not isinstance(classifier, sklearn.linear_model.LogisticRegression)):
            self.fail("Classifier is not a sklearn.linear_model.LogisticRegression.")

        classifier.predict(features)

        score = classifier.score(features, labels)
        if (not math.isclose(score, 1.0)):
            self.fail("Classifier was not trained properly (it could not score perfectly on idea data).")

        self.full_credit()

class T3B(autograder.question.Question):
    def score_question(self, submission):
        features = pandas.DataFrame({
            'a': [0, 1, 0, 1, 0, 1],
            'b': [1, 0, 1, 0, 1, 0],
        })

        labels = pandas.Series([True, False, True, False, True, False])

        classifier = submission.__all__.get_trained_dt(features, labels)
        self.check_not_implemented(classifier)

        if (not isinstance(classifier, sklearn.tree.DecisionTreeClassifier)):
            self.fail("Classifier is not a sklearn.tree.DecisionTreeClassifier.")

        classifier.predict(features)

        score = classifier.score(features, labels)
        if (not math.isclose(score, 1.0)):
            self.fail("Classifier was not trained properly (it could not score perfectly on idea data).")

        self.full_credit()

class T4A(autograder.question.Question):
    def score_question(self, submission):
        features = pandas.DataFrame({
            'a': [0, 1, 0, 1, 0, 1],
            'b': [1, 0, 1, 0, 1, 0],
        })

        labels = pandas.Series([True, False, True, False, True, False])

        lr_scores, dt_scores = submission.__all__.get_train_size_scores(features, labels, [2, 3, 4])
        self.check_not_implemented(lr_scores)

        if ((len(lr_scores) != 3) or (len(dt_scores) != 3)):
            self.fail("Incorrect number of scores returned.")

        for i in range(len(lr_scores)):
            if ((lr_scores[i] < 0) or (lr_scores[i] > 1.0)):
                self.fail("LR score out of range.")

            if ((dt_scores[i] < 0) or (dt_scores[i] > 1.0)):
                self.fail("DT score out of range.")

        # With randomization, at least four data points are required to get representation of all labels.
        if (not math.isclose(lr_scores[2], 1.0)):
            self.fail("LR classifier could not score perfectly on idea data.")

        if (not math.isclose(dt_scores[2], 1.0)):
            self.fail("DT classifier could not score perfectly on idea data.")

        self.full_credit()

class T4B(autograder.question.Question):
    def score_question(self, submission):
        features = pandas.DataFrame({
            'a': [0, 1, 0, 1, 0, 1],
            'b': [1, 0, 1, 0, 1, 0],
        })

        labels = pandas.Series([True, False, True, False, True, False])

        train_scores, test_scores = submission.__all__.get_dt_max_depth_scores(features, labels, [1, 2, 3], train_size = 4)
        self.check_not_implemented(train_scores)

        if ((len(train_scores) != 3) or (len(test_scores) != 3)):
            self.fail("Incorrect number of scores returned.")

        for i in range(len(train_scores)):
            if ((train_scores[i] < 0) or (train_scores[i] > 1.0)):
                self.fail("Train score out of range.")

            if ((test_scores[i] < 0) or (test_scores[i] > 1.0)):
                self.fail("Test score out of range.")

        if (not math.isclose(train_scores[1], 1.0)):
            self.fail("Classifier could not score perfectly on idea train data.")

        if (not math.isclose(test_scores[1], 1.0)):
            self.fail("Classifier could not score perfectly on idea test data.")

        self.full_credit()

class T5A(autograder.question.Question):
    def score_question(self, submission):
        data = pandas.DataFrame({
            'a': [1,   2,   3,   4,   5,   6],
            'b': [6.6, 3.3, 1.1, 2.2, 5.5, 4.4],
        })

        under_group, over_group = submission.__all__.split_on_column(data.copy(), 'a', 3.5)
        self.check_not_implemented(under_group)

        test_cases = [
            ('a', 3.5, 'sorted column, even split',
                    {'a': [1, 2, 3], 'b': [6.6, 3.3, 1.1]},
                    {'a': [4, 5, 6], 'b': [2.2, 5.5, 4.4]})
        ]

        self.full_credit()
        deduction = -(max(1, self.max_points // len(test_cases)))

        for (column_name, threshold, name, expected_under, expected_over) in test_cases:
            actual_under, actual_over = submission.__all__.split_on_column(data.copy(), column_name, threshold)

            # Reset indexes for comparisons.
            actual_under = actual_under.reset_index(drop = True)
            actual_over = actual_over.reset_index(drop = True)

            expected_under = pandas.DataFrame(expected_under).reset_index(drop = True)
            expected_over = pandas.DataFrame(expected_over).reset_index(drop = True)

            split_cases = [
                ('under', expected_under, actual_under),
                ('over', expected_over, actual_over),
            ]

            for (split, expected, actual) in split_cases:
                if (len(expected) != len(actual)):
                    self.add_message("Test case '%s': Number of %s rows is incorrect." % (name, split), add_score = deduction)
                    continue

                # DataFrame.equals() does not always work with empty frames.
                if (len(expected) == 0):
                    continue

                if (not expected.equals(actual)):
                    self.add_message("Test case '%s': Number of %s rows is correct, but contents are wrong." % (name, split), add_score = deduction)
                    continue

        self.cap_score()

class T5B(autograder.question.Question):
    def score_question(self, submission):
        clean_data = pandas.DataFrame({
            'group':   [0, 0, 0, 0, 1, 1, 1, 1],
            'feature': [1, 0, 1, 0, 1, 0, 1, 0],
            'label':   [1, 0, 1, 0, 1, 0, 1, 0],
        })

        disparity_data = pandas.DataFrame({
            'group':   [0, 0, 0, 0, 1, 1, 1, 1],
            'feature': [1, 0, 1, 0, 1, 0, 0, 1],
            'label':   [1, 0, 1, 0, 1, 0, 1, 0],
        })

        disparity = submission.__all__.compute_disparity(clean_data, 'group', 'label')
        self.check_not_implemented(disparity)

        if (not math.isclose(disparity, 0.0)):
            self.fail("Non-zero disparity returned on data with no disparity.")

        disparity = submission.__all__.compute_disparity(disparity_data, 'group', 'label')
        if (math.isclose(disparity, 0.0)):
            self.fail("Zero disparity returned on data with disparity.")

        self.full_credit()

class T5C(autograder.question.Question):
    def score_question(self, submission):
        clean_data = pandas.DataFrame({
            'group':   [0, 0, 0, 0, 1, 1, 1, 1],
            'feature': [1, 0, 1, 0, 1, 0, 1, 0],
            'label':   [1, 0, 1, 0, 1, 0, 1, 0],
        })

        disparity_data = pandas.DataFrame({
            'group':   [0, 0, 0, 0, 1, 1, 1, 1],
            'feature': [1, 0, 1, 0, 1, 0, 0, 1],
            'label':   [1, 0, 1, 0, 1, 0, 1, 0],
        })

        fnr_disparity, fpr_disparity = submission.__all__.compute_confusion_disparity(clean_data, 'group', 'label')
        self.check_not_implemented(fnr_disparity)

        for (name, disparity) in [('FNR', fnr_disparity), ('FPR', fpr_disparity)]:
            if (not math.isclose(disparity, 0.0)):
                self.fail("Non-zero %s disparity returned on data with no disparity." % (name))

        fnr_disparity, fpr_disparity = submission.__all__.compute_confusion_disparity(disparity_data, 'group', 'label')
        for (name, disparity) in [('FNR', fnr_disparity), ('FPR', fpr_disparity)]:
            if (math.isclose(disparity, 0.0)):
                self.fail("Zero %s disparity returned on data with disparity." % (name))

        self.full_credit()

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
    assignment = Lab1(input_dir = path)
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
