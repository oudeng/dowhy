"""Functions and classes in this module should be considered experimental, meaning there might be breaking API changes
in the future.
"""

from typing import List

import numpy as np
import sklearn
from packaging import version
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures

if version.parse(sklearn.__version__) < version.parse("1.0"):
    from sklearn.experimental import enable_hist_gradient_boosting  # noqa

from sklearn.ensemble import (
    AdaBoostClassifier,
    ExtraTreesClassifier,
    HistGradientBoostingClassifier,
    RandomForestClassifier,
)
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC

from dowhy.gcm.fcms import ClassificationModel
from dowhy.gcm.ml.regression import SklearnRegressionModel
from dowhy.gcm.util.general import apply_one_hot_encoding, shape_into_2d


class SklearnClassificationModel(SklearnRegressionModel, ClassificationModel):
    def predict_probabilities(self, X: np.array) -> np.ndarray:
        return shape_into_2d(self._sklearn_mdl.predict_proba(apply_one_hot_encoding(X, self._one_hot_encoders)))

    @property
    def classes(self) -> List[str]:
        return self._sklearn_mdl.classes_

    def clone(self):
        return SklearnClassificationModel(sklearn_mdl=sklearn.clone(self._sklearn_mdl))


def create_random_forest_classifier(**kwargs) -> SklearnClassificationModel:
    return SklearnClassificationModel(RandomForestClassifier(**kwargs))


def create_gaussian_process_classifier(**kwargs) -> SklearnClassificationModel:
    return SklearnClassificationModel(GaussianProcessClassifier(**kwargs))


def create_hist_gradient_boost_classifier(**kwargs) -> SklearnClassificationModel:
    return SklearnClassificationModel(HistGradientBoostingClassifier(**kwargs))


def create_logistic_regression_classifier(**kwargs) -> SklearnClassificationModel:
    return SklearnClassificationModel(LogisticRegression(**kwargs))


def create_extra_trees_classifier(**kwargs) -> SklearnClassificationModel:
    return SklearnClassificationModel(ExtraTreesClassifier(**kwargs))


def create_ada_boost_classifier(**kwargs) -> SklearnClassificationModel:
    return SklearnClassificationModel(AdaBoostClassifier(**kwargs))


def create_support_vector_classifier(**kwargs) -> SklearnClassificationModel:
    return SklearnClassificationModel(SVC(**kwargs))


def create_knn_classifier(**kwargs) -> SklearnClassificationModel:
    return SklearnClassificationModel(KNeighborsClassifier(**kwargs))


def create_gaussian_nb_classifier(**kwargs) -> SklearnClassificationModel:
    return SklearnClassificationModel(GaussianNB(**kwargs))


def create_polynom_logistic_regression_classifier(
    degree: int = 3, **kwargs_logistic_regression
) -> SklearnClassificationModel:
    return SklearnClassificationModel(
        make_pipeline(
            PolynomialFeatures(degree=degree, include_bias=False), LogisticRegression(**kwargs_logistic_regression)
        )
    )
