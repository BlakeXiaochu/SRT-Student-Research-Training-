class KCFtracker(object):
	import numpy as np
	from numpy.fft import fft2, ifft2
	"""
		object tracker of KCF algorithm
	"""
	__slot__ = {'alphaf', 'coefY', '_paddingTarget', '_cosWin'}
	def __init__(self):
		super(Tracker, self).__init__()
		self.alphaf = None
		#coeffient controling The regression targets y
		self.coefY = 10
		self	


	#according to input image patch, train a regression tracker 
	def train(self, paddingRegion, regLambda, method, **kw):
		'''
			paddingRegion	- image patch(region) that contains target
			regLambda		- regularization coeffient λ for ridge regression

			method 			- kernel method
			kw 				- parameters for different kernel method. including following method and corresponding parameter(s):
							  	1. Gaussian: sigma (exp(-1/sigma**2*x))
							  	2. polynomial: a, b ((x + a)**b)
		'''
		if not isinstance(paddingRegion, np,ndarray):
			print('argument 1: numpy.ndarray is required.')
			raise TypeError

		if not isinstance(bandwidth, float):
			print('argument 2: float is required.')
			raise TypeError

		imgSize = paddingRegion.shape

		#the input patches (either raw pixels or extracted feature channels) are weighted by a cosine window
		cosWin = np.reshape(np.hamming(imgSize[0]), [-1, 1]) * np.reshape(np.hamming(imgSize[1]), [1, -1])
		self._cosWin = cosWin
		paddingRegion = paddingRegion * cosWin
		self._paddingTarget = paddingRegion


		#the regression targets y
		s = np.sqrt(imgSize[0] * imgSize[1]) / self.coefY	#spatial bandwidth s, controling The regression targets y simply follow a Gaussian function
		coord = np.mgrid[-int(imgSize[0]/2):int(imgSize[0]/2 + 0.5), -int(imgSize[1]/2):int(imgSize[1]/2 + 0.5)]
		coordX = coord[0, :, :]
		coordY = coord[1, :, :]
		y = np.exp( -0.5 * (coordX**2 + coordY**2) / (s**2) )
		y = np.roll(y, (int(imgSize[0]/2 + 0.5), int(imgSize[1]/2 + 0.5)), axis = (0, 1))

		#regression
		k = kernelCorrelation(paddingRegion, paddingRegion, method, **kw)
		self.alphaf = fft2(y) / (fft2(k) + regLambda)

		return self.alphaf
		

	#run tracker, return relative position with the input image patch
	def detect(self, paddingRegion, method, **kw):`
		'''
			
		'''
		if self.alphaf is None:
			print('tracker has not been trained.')
			raise Exception

		#kernel correlation
		kxz = kernelCorrelation(paddingRegion * self._cosWin, self._paddingTarget, method, **kw)
		kf = fft2(kxz)

		#regression results in fourier domain
		ff = kf * self.alphaf
		f = np.real(ifft2(ff))
		maxPosition = np.argmax(f)

		#return relative position with the input image pacth
		imgSize = paddingRegion.shape[0:2]
		rePos = tuple(maxPosition // imgSize[1], maxPosition % imgSize[1])

		return rePos



	def kernelCorrelation(self, x1, x2, method, **kw):
		if (not isinstance(x1, np.ndarray)) or (not isinstance(x2, np.ndarray)):
			print('numpy.ndarray is required.')
			raise TypeError

		if (x1.ndim == 2) and (x2.ndim == 2):
			single = 1
		elif (x1.ndim == 3) and (x2.ndim == 3):
			single = 0
		else:
			print('2 or 3 dimension arrays are required.')
			raise ValueError

		if x1.shape != x2.shape:
			print('the input image pacthes do not match.')
			raise ValueError

		#linear regression
		if method == 'linear':
			if single:
				x12DotProdf = np.conj(fft2(x1)) * fft2(x2)
			else:
				x12DotProdf = np.sum( np.conj(fft2(x1), axes = (0, 1)) * fft2(x2, axes = (0, 1)) , axis = 2)

			x12DotProd = ifft2(x12DotProdf)
			return x12DotProd

		#Gaussian kernel
		elif method == 'gaussian':
			sigma = kw['sigma']
			x1Norm = np.sum(x1**2)
			x2Norm = np.sum(x2**2)

			if single:
				x12DotProdf = np.conj(fft2(x1)) * fft2(x2)
			else:
				x12DotProdf = np.sum( np.conj(fft2(x1), axes = (0, 1)) * fft2(x2, axes = (0, 1)) , axis = 2)

			x12DotProd = ifft2(x12DotProdf)
			k = np.exp( -(x1Norm + x2Norm - 2 * x12DotProd.real) / (sigma**2) / x12DotProd.size)
			return k

		#polynomial kernel
		elif method == 'polynomial':
			a = kw['a']
			b = kw['b']

			if single:
				x12DotProdf = np.conj(fft2(x1)) * fft2(x2)
			else:
				x12DotProdf = np.sum( np.conj(fft2(x1), axes = (0, 1)) * fft2(x2, axes = (0, 1)) , axis = 2)
			
			x12DotProd = ifft2(x12DotProdf)
			k = (x12DotProd.real + a)**b
			return k

		#wrong method type
		else:
			print('invalid kernel method.')
			raise ValueError




