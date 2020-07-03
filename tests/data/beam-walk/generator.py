#!/usr/bin/python
import sys
import os

def generate_instance( size ) :
	output_lines = []
	# Read template and substitute as appropiate
	with open( 'instance-template.pddl' ) as instream :
		for line in instream :
			line = line.strip()
			if "@problem_name@" in line :
				out_line = line.replace( "@problem_name@", "beam-walk-%d"%size )
				output_lines.append( out_line )
				continue
			if "@objects_def@" in line :
				obj_names = []
				for i in range(0,size) :
					obj_names.append( 'p%d'%i )
				obj_names_txt = " ".join( obj_names ) + " - location"
				out_line = line.replace( "@objects_def@", obj_names_txt )
				output_lines.append( out_line )
				continue
			if "@next_fwd@" in line :
				preds = []
				for i in range(0,size-1) :
					preds.append( '(next-fwd p%d p%d)'%(i,i+1) )
				preds_txt = " ".join( preds )
				out_line = line.replace( "@next_fwd@", preds_txt )
				output_lines.append( out_line )
				continue
			if "@next_bwd@" in line :
				preds = []
				for i in range(1, size ) :
					preds.append( '(next-bwd p%d p%d)'%(i,i-1) )
				preds_txt = " ".join( preds )
				out_line = line.replace( "@next_bwd@", preds_txt )
				output_lines.append( out_line )
				continue
			if "@goal_position@" in line :
				literal = '(position p%d)'%(size-1)
				out_line = line.replace( "@goal_position@", literal )
				output_lines.append( out_line )
				continue
			output_lines.append( line )

	# Write generated instance
	output_filename = os.path.join( 'instances', 'p-%d.pddl'%size )
	with open( output_filename, 'w' ) as outstream :
		for line in output_lines :
			print >> outstream, line	
			
def usage() :

	print >> sys.stderr, "Missing arguments"
	print >> sys.stderr, "./generator <initial size> <max size> <increment>"
	print >> sys.stderr
	print >> sys.stderr, "Increment can be given as:"
	print >> sys.stderr, "\t+n to indicate an additive increase in size by n"
	print >> sys.stderr, "\txn to indicate a multiplicative increase in size by n"
	

def main() :

	if len(sys.argv) < 4 :
		usage()
		sys.exit(1)

	start_size = int(sys.argv[1])
	end_size = int(sys.argv[2])
	
	add_inc = lambda x, y : x + y
	mult_inc = lambda x, y : x * y
	inc = None
	delta = 1
	
	try :
		delta = int( sys.argv[3][1:] )
	except ValueError :
		print >> sys.stderr, "Factor to increase sizes needs to be an integer number"
		sys.exit(1)
	

	if sys.argv[3][0] == 'x' :
		inc = mult_inc
		if delta <= 1 :
			print >> sys.stderr, "Invalid increment value for multiplicative factor (needs to be greater than one)"
			sys.exit(1)
	elif sys.argv[3][0] == '+' :
		inc = add_inc
		if delta < 1 :
			print >> sys.stderr, "Invalid increment value for additive factor (needs to be greater than zero)"
			sys.exit(1)
	else :
		print >> sys.stderr, "'%s' is not a valid type of increment"%sys.argv[3][0]
		print >> sys.stderr, "Please use either +%s or x%s, to denote an additive (multiplicative) increment by %s"%(sys.argv[3][1:],sys.argv[3][1:], sys.argv[3][1:])
		sys.exit(1)

	print >> sys.stdout, "Deleting instances..."
	os.system( 'rm -rf instance/*.pddl' )
	
	size = start_size
	
	while size <= end_size :
		print >> sys.stdout, "Generating problem with size =", size		
		generate_instance( size )
		size = inc(size, delta)
	

if __name__ == '__main__' :
	main()
