Simple Vp-Tree
==============


A Pure python implementation of vp_tree.
Is a simple but yet powerfull implementation of
a vp-tree. It implements a simple knn search and
will implement a way to persist the tree.


Links
-----

* `<http://en.wikipedia.org/wiki/Vantage-point_tree>`_
* `<http://en.wikipedia.org/wiki/K-nearest_neighbors_algorithm>`_

Hello, world
------------

Here is a simple "Hello, world" example web app for Tornado::


    from simple_vp import *


    rn = lambda: random.randint(0, 10000)
    aset = [(rn(), rn()) for i in range(40000)]
    q = (rn(), rn())
    rad = 9990
    max_results = 30
    distance = lambda a, b: math.sqrt(sum([((x-y)**2) for x, y in zip(a, b)]))

    s = time.time()
    print "creating..."
    root = VpNode(aset, distance=distance)
    print "done", time.time() - s
    s = time.time()
    print "searching..."

    se = VpSearch(root, q, rad, max_results ) 
    out = se.knn()
    for k,v in sorted(se.stat.items()):
        print k,v

    print "out: %s" % len(out)
    print "done", time.time() - s



In this example is performed a knn search in a 2d set with random
points.

Installation
------------

.. parsed-literal::


    git clone ...
    python setup.py build
    sudo python setup.py install


