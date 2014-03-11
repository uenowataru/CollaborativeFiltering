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
				if (ratings[i][j] > 0):
					sumratings += ratings[i][j]
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
						numA = ratings[i][k] - avgr_i
						numB = ratings[j][k] - avgr_j
						sigmaA += numA * numA
						sigmaB += numB * numB
						covariance += numA * numB
					sigmas = math.sqrt(sigmaA) * math.sqrt(sigmaB)
					#print sigmas, commonitems
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
			for j in range(num_items):
				sumdeviation = 0.0
				sumweights = 0.0
				for k in range(num_users):
					if(k!=i and ratings[k][j] != 0):
						residual = ratings[k][j] - user_means[k]
						sumdeviation += residual * weights[i][k]
						sumweights += math.fabs(weights[i][k])
				predictions[i][j] = user_means[i]
				if(sumweights > 0):
					predictions[i][j] += sumdeviation / sumweights


if __name__ == "__main__":
	ratings = [[4,3,3,3,2], [4,3,3,3,0], [4,2,2,0,5], [4,1,1,1,1]]
	cf = CollaborativeFiltering(ratings)
	print "prediction(1,4):",cf.getPredictions(1, 4), "should equal 3.3"
	print "prediction(2,3):",cf.getPredictions(2, 3), "should equal 2.96.."


