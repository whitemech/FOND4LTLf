import sys
import numpy as np

if len(sys.argv) != 9:
	print('Wrong usage, you should use python name.py N1 N2 N3 M R BG GG fname')
	# (N1+N2+N3)xM grid, R rocks, BG bad golds, GG good golds
	exit()

N1 = int(sys.argv[1])
N2 = int(sys.argv[2])
N3 = int(sys.argv[3])
N = N1 + N2 + N3
M = int(sys.argv[4])
R = int(sys.argv[5])
BG = int(sys.argv[6])
GG = int(sys.argv[7])
nameTask = sys.argv[8]

task = open(nameTask, 'w')

task.write('(define (problem miner-0)')
task.write('\n')
task.write('(:domain miner)')
task.write('\n')
task.write('(:objects ')
task.write('\n')
for i in xrange(N):
	for j in xrange(M):
		task.write('\tL%i%i - location' % (i + 1, j + 1))
		task.write('\n')
task.write('\n')
for i in xrange(R):
	task.write('\tr%i - rock' % (i + 1))
	task.write('\n')
task.write(')')
task.write('\n')

task.write('(:init')
task.write('\n')

task.write('\t(person-alive)\n')
task.write('\t(person-at L%i%i)\n' % (1, 1))
task.write('\t(goldcount-0)\n')
task.write('\t(botton-loc L11)\n')
task.write('\n')

#R_3 = int(np.ceil(R / 3))
#for i in xrange(R_3):
#	r1 = i * 3 + 0
#	r2 = i * 3 + 1
#	r3 = i * 3 + 2
#	task.write('\t(rock-at r%i L%i%i)\n' % (r1 + 1, np.random.randint(N1) + 1, np.random.randint(M) + 1))
#	task.write('\t(rock-at r%i L%i%i)\n' % (r2 + 1, N1 + np.random.randint(N2) + 1, np.random.randint(M) + 1))
#	task.write('\t(rock-at r%i L%i%i)\n' % (r3 + 1, N1 + N2 + np.random.randint(N3) + 1, np.random.randint(M) + 1))

for i in xrange(R):
	task.write('\t(rock-at r%i L%i%i)\n' % (i + 1, np.random.randint(N1) + 1, np.random.randint(M) + 1))

task.write('\n')
count = 0
locations = set()
while count < BG:
	pos = (np.random.randint(N1) + 1, np.random.randint(M) + 1)
	if pos in locations:
		continue
	else:
		count += 1
		task.write('\t(gold-bad-at L%i%i)\n' % (pos[0], pos[1]))
		locations.add(pos)

task.write('\n')
count = 0
locations = set()
while count < GG:
	pos = (N1 + N2 + np.random.randint(N3) + 1, np.random.randint(M) + 1)
	if pos in locations:
		continue
	else:
		count += 1
		task.write('\t(gold-good-at L%i%i)\n' % (pos[0], pos[1]))
		locations.add(pos)

task.write('\n')
deltaF = [-1, 1, 0, 0]
deltaC = [0, 0, 1, -1]
for i in xrange(N):
	for j in xrange(M):
		f = i + 1
		c = j + 1
		for df, dc in zip(deltaF, deltaC):
			x = f + df
			y = c + dc
			if x <= 0 or y <= 0 or x > N or y > N:
				continue
			else:
				task.write('\t(road L%i%i L%i%i)' % (f, c, x, y))
				task.write('\n')

task.write(')')
task.write('\n')

task.write('(:goal (and (person-alive) (goldcount-3)))')
task.write('\n')
task.write(')')

task.close()