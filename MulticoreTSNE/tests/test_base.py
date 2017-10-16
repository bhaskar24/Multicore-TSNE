import unittest
from functools import partial

import numpy as np

from sklearn.datasets import make_blobs
from sklearn.metrics import pairwise_distances

from MulticoreTSNE import MulticoreTSNE


make_blobs = partial(make_blobs, random_state=0)


def pdist(X):
    """Condensed pairwise distances, like scipy.spatial.distance.pdist()"""
    return pairwise_distances(X)[np.triu_indices(X.shape[0], 1)]


class TestMulticoreTSNE(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.Xy = make_blobs(20, 100, 2, shuffle=False)

    def test_tsne(self):
        X, y = self.Xy
        tsne = MulticoreTSNE(perplexity=5, n_iter=500, random_state=0)
        E = tsne.fit_transform(X)

        self.assertEqual(E.shape, (X.shape[0], 2))

        max_intracluster = max(pdist(E[y == 0]).max(),
                               pdist(E[y == 1]).max())
        min_intercluster = pairwise_distances(E[y == 0],
                                              E[y == 1]).min()

        self.assertGreater(min_intercluster, max_intracluster)

    def test_n_jobs(self):
        X, y = self.Xy
        tsne = MulticoreTSNE(perplexity=5, n_iter=100, n_jobs=-2)
        tsne.fit_transform(X)
