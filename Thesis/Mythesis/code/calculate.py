from scipy import stats
import numpy as np

def slope(x,y):

	slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)
	return slope

print(slope(np.array([4,8]),np.array([8,16])))