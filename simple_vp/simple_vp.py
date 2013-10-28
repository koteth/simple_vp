import random
import math
import json
from itertools import count
from operator import itemgetter
import time
import heapq

crit = lambda q, r, p, distance: distance(p, q) <= r
choose_left = lambda q, r, n: n.distance(n.pivot, q) - r <= n.median
choose_right = lambda q, r, n: n.distance(n.pivot, q) + r >= n.median


class VpNode(object):
    ids = count(0)

    __slots__ = ('is_leaf', 'aset', 'level', 'distance',
                 'pivot', 'dist_set', 'median', 'left', 'right',
                 'type')

    def __init__(self, aset=[], distance=None, level=0,
                 median=None):
        self.ids.next()
        self.is_leaf = True
        self.aset = aset
        self.level = level
        self.type = 'root'
        self.distance = distance
        self.pivot = aset[0]
        if len(aset) > 1:
            self._set_non_leaf_params()

    def _set_non_leaf_params(self):
        self.is_leaf = False
        self.pivot = self._get_pivot()
        self.dist_set = self._get_dist_set()
        self.median = self._get_median()
        nodes = [VpNode(ch, level=self.level + 1,
                 distance=self.distance)
                 for ch in self._split_set()]
        nodes[0].type = 'l'
        nodes[1].type = 'r'
        self.left, self.right = nodes[0], nodes[1]

    def _get_dist_set(self):
        dist_p = lambda x: self.distance(x, self.pivot)
        dist_set = ((x, dist_p(x)) for x in self.aset)
        return sorted(dist_set, key=lambda x: x[1])

    def _get_median(self):
        return self.dist_set[len(self.dist_set) // 2][1]

    def _get_pivot(self):
        return random.choice(self.aset)

    def _split_set(self):
        hl = len(self.dist_set) // 2
        out = (self.dist_set[:hl], self.dist_set[hl:])
        return (map(itemgetter(0), v) for v in out)

    def dump(self):
        o = [ self._str_obj() ]
        if not self.is_leaf:
            o += self.left.dump()
            o += self.right.dump()
        return o

    def _str_obj(self):
        st_obj = {'_id': id(self), 'is_leaf': self.is_leaf,
                  'level': self.level, 'type': self.type,
                  'pivot': self.pivot}
        if self.is_leaf:
            st_obj.update({'point': self.aset[0]})
        else:
            st_obj.update({'left': id(self.left),
                           'right': id(self.right)})
        return st_obj

  
    def __str__(self):
        st_obj = _str_obj(self)
        return json.dumps(st_obj)


class VpSearch(object):

    def __init__(self, root, query, rad, max_n=20):
        self.root = root
        self.query = query
        self.rad = rad
        self.knnrad = rad
        self.stat = {}
        self.heap = []
        self.results = []
        self.knnresults = []
        self.recursion = 0
        self.distance = root.distance
        self.max_n = max_n

    def _incr_stat(self, label):
        self.stat[label] = self.stat.get(label, 0) + 1

    def knn(self):
        self.stat = {}
        self._knn(self.root, self.query)
        self.knnresults = [heapq.heappop(self.knnresults)
                           for i in range(min(self.max_n, len(self.knnresults)))]
        return [x[1]for x in self.knnresults]

    def _knn(self, node, q):
        if node.is_leaf:
            for i in node.aset:
                i = (self.distance(i, self.query), i)
                heapq.heappush(self.knnresults, i)
            if len(self.knnresults) > self.max_n+1:
                self.knnrad = min(self.knnresults[self.max_n+1][0], self.knnrad)
            return

        for n, c in ((node.left, choose_left), (node.right, choose_right)):
            if c(q, self.knnrad, node):
                self._knn(n, q)
                self._incr_stat('expanded')
            else:
                self._incr_stat('skipped level:%s' % n.level)
