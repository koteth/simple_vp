from simple_vp import *
import time


def main():

    rn = lambda: random.randint(0, 10000)
    aset = [(rn(), rn()) for i in range(40000)]
    q = (rn(), rn())
    rad = 9990
    distance = lambda a, b: math.sqrt(sum([((x-y)**2) for x, y in zip(a, b)]))

    s = time.time()
    print "creating..."
    root = VpNode(aset, distance=distance)
    print "done", time.time() - s
    s = time.time()
    print "searching..."

    #print root.dump()
    se = VpSearch(root, q, rad, 30)
    #out = se.search()
    out = se.knn()
    for k, v in sorted(se.stat.items()):
        print k, v

    print "out: %s" % len(out)
    print "done", time.time() - s

    try:
        import pylab as plt
        projx = lambda x: map(lambda y: y[0], x)
        projy = lambda x: map(lambda y: y[1], x)
        fig, ax = plt.subplots()
        ax.scatter(projx(aset), projy(aset), 20)
        ax.scatter([q[0]], [q[1]], 20, color='g')
        ax.scatter(projx(out), projy(out), 20, color='r')

        ax.annotate("query", xy=q)
        plt.show()
    except:
        pass

if __name__ == '__main__':
    main()
