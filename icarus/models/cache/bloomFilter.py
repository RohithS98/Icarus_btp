from math import floor, modf

class bloomFilter:
	def __init__(self, n):
		self.arr = [0 for i in range(n)]
		self.n = n
		self.num = 0
	
	def hash1(self, k):
		c = 0.618033988
		return floor(self.n * modf(k*c)[0])
		
	def hash2(self, k):
		c = 0.3302954
		return floor(self.n * modf(k*c)[0])
	
	def insert(self, k):
		a, b = self.hash1(k), self.hash2(k)
		self.arr[a] = 1
		self.arr[b] = 1
		self.num += 1
	
	def check(self, k):
		a, b = self.hash1(k), self.hash2(k)
		if self.arr[a] == self.arr[b] == 1:
			return True
		return False
	
	def clear(self):
		self.arr = [0 for i in range(n)]
		
	def getNum(self):
		return self.num
		
		
a = bloomFilter(100)
inserts = [10,20,30,56,283,956,83928,43875,1928,283]
checks = [10,20,30,56,283,956,83928,43875,1928,283,873,72348723, 1283,8238]
for i in inserts:
	a.insert(i)
for i in checks:
	f = a.check(i)
	if f == (i in inserts):
		print("Correct")
	elif f == False:
		print("Not Found")
	else:
		print("False positive")
