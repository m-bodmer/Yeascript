import re, sys

Operators = {
	# Number operations
	'NumbersMan' : {
		'AddBro' : '+',
		'SubtractBro' : '-',
		'MultiplyBro' : '*',
		'DivideBro' : '/',
	},

	#Program control operations
	'ProgramMan' : {
		'ZeroMan' : 'ifzero',
		'PositiveMan' : 'ifpos',
		'NegativeMan' : 'ifneg',
		'LabelMan' : 'label',
		'GotoMan' : 'goto',
	},

	'StackMan' : {
		'DiscardBro' : 'discard',
		'SwapMan' : 'swap',
		'DuplicateBro' : 'duplicate',
	},

	#Output operations
	'OutputMan' : {
		'GaneshMan' : 'charOut',
		'AndrewMan' : 'numOut',
	},

	#Values
	"HeyMan" : 'value'
}

class CoolMan:
	def __init__(self, input=None):
		# Set up global lists 
		self.tokens = []
		self.stack = []
		if input:
			self.input = input
		else:
			self.input = []

	def output(self):
		print self.parse(self.input)

	def parse(self, input):
		if not input:
			return

		if isinstance(input, str):
			input = [input]

		#Build our stack
		self.tokenize(input)
		i = 0
		output = ''

		#Time to go through our stack
		while i < len(self.tokens):
			item = self.tokens[i]
			#Check if our item is a decimal number
			if not isinstance(item, str):
				#If it exists in the dictionary, append the decimal number
				try:
					self.stack.append(int(item))
				except KeyError:
					self.stack.append(0)
			#Check to see if the token is anything else besides a number
			elif item in '+-*/%':
				self.stack.append(self.operation(self.stack, item))
				#print self.stack
			elif item.startswith('label'):
				pass
			elif item.startswith('goto'):
				label = re.split('\W+', item)[1]
				i = self.tokens.index('label-' + label)
			#Output a Character
			elif item == 'charOut':
				output += chr(self.stack.pop())
			#Output a Number
			elif item == 'numOut':
				x = self.stack.pop()
				output += str(x)
			elif item == 'duplicate':
				first = self.stack.pop()
				self.stack.append(first)
				self.stack.append(first)
			elif item == 'swap':
				first = self.stack.pop()
				second = self.stack.pop()
				self.stack.append(first)
				self.stack.append(second)
			elif item == 'discard':
				self.stack.pop()
			elif item.startswith('ifzero'):
				first = self.stack.pop()
				if first == 0:
					label = re.split('\W+', item)[1]
					i = self.tokens.index('label-' + label)
			elif item.startswith('ifpos'):
				first = self.stack.pop()
				if first > 0:
					label = re.split('\W+', item)[1]
					i = self.tokens.index('label-' + label)
			elif item.startswith('ifneg'):
				first = self.stack.pop()
				if first < 0:
					label = re.split('\W+', item)[1]
					i = self.tokens.index('label-' + label)
			else:
				pass
			i += 1

		self.tokens = []
		if output:
			return output
		else:
			if self.stack:
				return self.stack[-1]
			else:
				return None

	def operation(self, stack, op):
		#Perform an operation between two values
		first = stack.pop()
		second = stack.pop()
		return eval(str(second) + op + str(first))

	def tokenize(self, input):
		for line in input:

			#Allow comments denoted by //
			if line.startswith('//'):
				continue
			#Create a list of operators for each line
			ops = re.split('\s+', line)
			#print "Line: "
			#print ops

			#Remove any blank strings from the operator list that may have been created when splitting
			ops = [op for op in ops if op]

			for op in ops:
				#print "Op: "
				#print op
				#Create a list for each operator, looking for any - characters
				parse_list = re.split('\W+', op)
				#print "Parse List: "
				#print parse_list
				identifier = parse_list[0]
				#print "Identifier: " + identifier

				if identifier in Operators:
					prefix = Operators[identifier]
					subop = parse_list[1]

					if prefix == 'value':
						#Create a translation table to map the sub operator to a binary string
						#Convert the binary string to decimal
						#Yea represents a 0, YeaMan represents a 1
						subop = subop.replace('YeaMan', '1');
						binarystring = subop.replace('Yea', '0')

						decimalNum = int(binarystring, 2)
						self.tokens.append(decimalNum)
					elif subop in prefix:
						#Look up sub operators 
						sub_id = prefix[subop]
						if sub_id == 'label' or sub_id=='goto' or sub_id.startswith('if'):
							sub_id+= '-' + ops[1]
						self.tokens.append(sub_id)
		#print self.tokens

# Run as standalone program with file input
if __name__ == '__main__':
	if len(sys.argv) == 2:
		try:
			file = open(sys.argv[1])
			cool = CoolMan(file)
			cool.output()
		except IOError:
			print 'File %s cannot be found' % sys.argv[0]
			sys.exit()
		