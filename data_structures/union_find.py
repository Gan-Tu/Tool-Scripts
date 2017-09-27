class UnionFind:

	def __init__(self):
		self.parents = {}
		self.rank = {}

	def find(self, n):
		"""Return the parent of node n"""
		if n not in self.parents:
			self.parents[n] = n
			self.rank[n] = 0
			return n
		elif self.parents[n] == n:
			return n
		else:
			# path compression, recursive
			self.parents[n] = self.find(self.parents[n])
			return self.parents[n]

	def samePartition(self, v1, v2):
		return self.find(v1) == self.find(v2)
			
	def union(self, v1, v2):
		v1_p = self.find(v1)
		v2_p = self.find(v2)
		# join smaller tree to larger tree
		if self.rank[v1_p] > self.rank[v2_p]:
			self.parents[v2] = v1_p
		else:
			self.parents[v1] = v2_p
			# rank adjustment
			if self.rank[v1_p] == self.rank[v2_p]:
				self.rank[v2_p] += 1