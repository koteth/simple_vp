from simple_vp import *
import time
import pylab as plt


def main():
    rn = lambda: random.randint(0, 6000)
    aset = [(rn(), rn(), rn(), rn() , rn(), rn(), rn()) for i in range(400000)]
    q = (rn(), rn(), rn(), rn(), rn(), rn(), rn())
    rad = 1000

    distance = lambda a, b: math.sqrt(sum([((x-y)**2) for x, y in zip(a, b)]))

    s = time.time()
    print "\ninput set %s points" % len(aset)
    print "creating tree..."
    root = VpNode(aset, distance=distance)
    print "created: %s nodes" % VpNode.ids
    print "done in s: %s" % (time.time() - s)
    s = time.time()
    print "searching..."


    #print root.dump()
    se = VpSearch(root, q, rad, 30 ) 
    #out = se.search()
    out = se.knn()
    for k,v in sorted(se.stat.items()):
        print k,v

    print "out: %s" % len(out)
    print "done", time.time() - s


    print "founded %s results" % len(out)
    print "done in s: %s" % (time.time() - s)

    projx = lambda x: map(lambda y: y[0], x)
    projy = lambda x: map(lambda y: y[1], x)
    
    print "max distance result set: ", max([distance(q,x) for x in out])
    s = set(aset)
    s = s.difference(set(out))
    print "min distance excluded set: ", min([distance(q,x) for x in s])


import cProfile

if __name__ == '__main__':
    main()
    #cProfile.run('main()')
    
