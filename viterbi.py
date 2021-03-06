###############################################
# Viterbi implementation					            #
# source code: wikipedia,					            #
#  - adjusted for sequence with 'end' state   #
#  - notation adjusted as shown in durbin	    #
###############################################

def print_vitMatrix(V):
	"""
	print v[i][k] as matrix
	- v[i][k]:
	- probabilities of the most probably path ending in state k 
	  w/observation i is known for all the states K
	"""

	print "	",
	for i in range(len(V)): print "%7d" % i,
	print
 
	for y in V[0].keys():
		print "%.8s: " % y,
		for t in range(len(V)):
			print "%.8s" % ("%f" % V[t][y]),
		print
 
def viterbi(obs, states, start_p, trans_p, emit_p, no_end=True):
	"""
	Given the obs and hmm(emission and transition),
	find the most probably path
	#no_end: without end state
	"""
	if no_end:
		L = len(obs)
	else:
		L = len(obs)-1 #excluding the end state
		
	V = [{}]
	path = {}
 
	# Initialization (i = 0)
	for k in states:
		V[0][k] = start_p[k] * emit_p[k][obs[0]]
		path[k] = [k]
 
	# Recursion (i = 1, ...L)
	for i in range(1,L):
		V.append({})
		newpath = {}
		for k in states:
			#v[l][i] = max(v[k][i-1]a[k][l]) * e[l][i]
			(prob, state) = max([(V[i-1][k0] * trans_p[k0][k] *\
								  emit_p[k][obs[i]], k0) for k0 in states])
			V[i][k] = prob
			newpath[k] = path[state] + [k]
 
		# update the path
		path = newpath
	
	# termination
	if no_end:
		(prob, state) = max([(V[L-1][y], y) for y in states])
		print_vitMatrix(V)
		return (prob, path[state])
	
	#with end state
	(vi_max_t,t_state) = max([(V[L-1][k] *\
							   trans_p[k]['end'],k)for k in states])
	V.append({})
	for y in states:
		prob = V[L-1][y]*trans_p[y]['end']
		V[L][y] = prob
	print_vitMatrix(V)
	return (vi_max_t, path[t_state])

if __name__=="__main__":
  states = ('Healthy', 'Fever')
  observations = ('normal', 'cold', 'dizzy')
  start_probability = {'Healthy': 0.6, 'Fever': 0.4}
  transition_probability = {
   'Healthy' : {'Healthy': 0.7, 'Fever': 0.3},
   'Fever' : {'Healthy': 0.4, 'Fever': 0.6},
   }
  emission_probability = {
   'Healthy' : {'normal': 0.5, 'cold': 0.4, 'dizzy': 0.1},
   'Fever' : {'normal': 0.1, 'cold': 0.3, 'dizzy': 0.6},
   }
  viterbi(observations,
                   states,
                   start_probability,
                   transition_probability,
                   emission_probability, no_end=True)

