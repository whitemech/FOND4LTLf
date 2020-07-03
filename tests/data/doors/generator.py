import sys

N = int(sys.argv[1])
fname = sys.argv[2]
with open(fname, 'w') as pf:
	pf.write('(define (problem doors-0)\n(:domain doors)\n(:objects\n')
	
	for i in range(N):
		pf.write('L%i - location\n' % (i + 1))
	for i in range(N-1):
		pf.write('D%i - door\n' % (i + 2))
	pf.write(')\n(:init\n(player-at L1)\n(initial-location L1)\n')

	for i in range(N-1):
		pf.write('(open D%i)\n' % (i + 2))

	for i in range(N-1):
		pf.write('(door-in D%i L%i)\n' % (i + 2, i + 2))

	for i in range(N-1):
		pf.write('(door-out D%i L%i)\n' % (i + 2, i + 1))

	pf.write('(final-location L%i)\n)\n' % (N))

	pf.write('(:goal (player-at L%i)))' % (N))
