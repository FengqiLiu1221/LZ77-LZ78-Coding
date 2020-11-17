import sys, math

def c(x):
	# x -> C(x)
	# may replaced by any coding scheme
	return x

def dc(cx):
	# C(x) -> x
	return cx

class LZ78:
	def __init__(self, s):
		self.s = s
		self.encoding = []
		self.entry_to_index = {(): -1}

	def encode(self):
		cur = 0
		MAX_LEN = len(self.s)
		buffer = []

		while True:
			if cur == MAX_LEN:
				cur_byte = 'EOF'
				buffer.append(cur_byte)
				tp = tuple(buffer)
				last_index = self.entry_to_index[tp[:-1]]
				self.encoding.append((last_index, c(cur_byte)))
				self.entry_to_index[tp] = len(self.encoding) - 1
				break

			cur_byte = self.s[cur]
			buffer.append(cur_byte)
			tp = tuple(buffer)

			if tp in self.entry_to_index:
				cur += 1
				continue

			last_index = self.entry_to_index[tp[:-1]]
			self.encoding.append((last_index, c(cur_byte)))
			self.entry_to_index[tp] = len(self.encoding) - 1
			buffer.clear()
			cur += 1

	def _find_entry(self, last_index, codeword):
		rs = [dc(codeword)]
		if last_index == -1:
			return rs

		prev_last_index, prev_codeword = self.encoding[last_index]
		rs += self._find_entry(prev_last_index, prev_codeword)
		return rs


	def decode(self):
		s = []
		for last_index, codeword in self.encoding:
			tmp = self._find_entry(last_index, codeword)
			tmp.reverse()
			s += tmp
		return ''.join(s[:-1])


	def save_file(self, path):
		file = open(path, 'w')
		for last_index, codeword in self.encoding:
			file.write(str(last_index) + ' ' + str(codeword) + '\n')
		file.close()


if __name__ == '__main__':

	file = open('Introduction to Data Compression.txt','r', encoding='UTF-8')
	s = file.read()
	file.close()

	encoder = LZ78(s)
	encoder.encode()
	
	print('----- Statistics -----')
	print('Original file size:', len(s), 'bytes')
	print('# Encoding entries:', len(encoder.encoding), '\n')

	print('Size after compression (byte base):', len(encoder.encoding) * (math.ceil(math.log(len(encoder.encoding), 256)) + 1), 'bytes')
	print('Compression rate:', len(encoder.encoding) * (math.ceil(math.log(len(encoder.encoding), 256)) + 1) / len(s), '\n')
	
	compression_size = 0
	for _, codeword in encoder.encoding:
		compression_size += math.log(len(encoder.encoding), 2) + len(codeword) * 8

	print('Size after compression (bit base):', math.ceil(compression_size / 8), 'bytes')
	print('Compression rate:', math.ceil(compression_size / 8) / len(s))

	new_s = encoder.decode()

	file = open('test_LZ78.txt', 'w',encoding='UTF-8')
	file.write(new_s)
	file.close()
