import math
class CollaborativeFiltering:
	def __init__(self, ratings):
		self.ratings =  ratings
		
		self.num_users = len(ratings)
		self.num_items = len(ratings[0])

		self.weights = [[0]*self.num_users for x in range(self.num_users)]
		self.user_means = [0 for x in range(self.num_users)]
		self.predictions = [[0]*self.num_items for x in range(self.num_users)]

		self.calculateMeans()
		self.calculateWeights()
		self.calculatePredictions()

	def getPredictions(self, userindex, itemindex):
		#return self.predictions
		return self.predictions[userindex][itemindex]

	def calculateMeans(self):
		for i in range(self.num_users):
			sumratings = 0.0
			counter = 0
			for j in range(self.num_items):
				if (self.ratings[i][j] > 0):
					sumratings += self.ratings[i][j]
					counter+=1
			if counter > 0:
				self.user_means[i] =  sumratings/counter

	def calculateWeights(self):
		ratings = self.ratings
		for i in range(self.num_users):
			for j in range(self.num_users):
				sum_i = 0.0
				sum_j = 0.0
				counter = 0
				commonitems = []
				for k in range(self.num_items):
					if(ratings[i][k]!=0 and ratings[j][k]!=0):
						sum_i += ratings[i][k]
						sum_j += ratings[j][k]
						commonitems.append(k)
						counter += 1
				if(counter > 1):
					avgr_i = sum_i/counter
					avgr_j = sum_j/counter

					covariance = 0.0
					sigmaA = 0.0
					sigmaB = 0.0
					for k in commonitems:
						devA = ratings[i][k] - avgr_i
						devB = ratings[j][k] - avgr_j
						sigmaA += devA * devA
						sigmaB += devB * devB
						covariance += devA * devB
					sigmas = math.sqrt(sigmaA) * math.sqrt(sigmaB)
					if(sigmas != 0):
						self.weights[i][j] = covariance / sigmas
					else:
						self.weights[i][j] = 0



	def calculatePredictions(self):
		num_users = self.num_users
		num_items = self.num_items
		user_means = self.user_means
		ratings = self.ratings
		weights = self.weights
		predictions = self.predictions

		for i in range(num_users):
			for m in range(num_items):
				sumdeviation = 0.0
				sumweights = 0.0
				for j in range(num_users):
					if(j!=i and ratings[j][m] != 0 and ratings[i][m]!=0):
						residual = ratings[j][m] -  user_means[j]
						sumdeviation += residual * weights[i][j]
						sumweights += math.fabs(weights[i][j])
				predictions[i][m] = user_means[i]
				if(sumweights > 0):
					predictions[i][m] += sumdeviation / sumweights














if __name__ == "__main__":
	
	ratings = [[4,3,3,3,2], [4,3,3,3,0], [4,2,2,0,5], [4,1,1,1,1]]
	cf = CollaborativeFiltering(ratings)
	print "prediction(1,4):",cf.getPredictions(1, 4), "should equal 3.25"
	print "prediction(2,3):",cf.getPredictions(3, 3), "should equal 1.46.." 
	'''
	ratings2 = [[5, 2, 5, 5, 1, 0],
		[3, 3, 3, 3, 3, 3],
		[2, 4, 3, 3, 4, 4],
		[2, 3, 2, 3, 2, 5],
		[5, 3, 5, 5, 5, 2]]
	cf = CollaborativeFiltering(ratings2)
	
	print [cf.getPredictions(0,i) for i in range(len(ratings2[0]))]
	'''
