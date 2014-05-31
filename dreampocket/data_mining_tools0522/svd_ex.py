from scipy import linalg, mat, dot;

U = None
s = None
V = None
matrix = None

def decomposition(ma):
	global matrix
	global U
	global s
	global V
	matrix = mat(ma);
	print "Original matrix:"
	print matrix
	U, s, V = linalg.svd( matrix )
#	print "U:"
#	print U
	print "sigma:"
	print s
#	print "VT:"
#	print V

def construction(num):
	global matrix
	global U
	global s
	global V
	loc = num
	rows,cols = matrix.shape
	#Dimension reduction, build SIGMA'
	for index in xrange(loc, len(s)):
		s[index]=0
	print "reduced sigma:"
	print s
	#Reconstruct MATRIX'
	reconstructedMatrix= dot(dot(U,linalg.diagsvd(s,len(matrix),len(V))),V)
	#Print transform
	print "reconstructed:"
	print reconstructedMatrix

decomposition([[500,701,3,4,1], [392,400,1,2,1],[589,543,1,1,2]])
construction(2)