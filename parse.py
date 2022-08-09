with open('state.txt', 'r') as f:
	parseTax = {}
	keys = []
	data = f.read().split(' ')
	for index, num in enumerate(data):
		if num in parseTax.keys():
			data[index] = str(parseTax[num])
		else:
			switch = 0
			while switch in keys:
				switch += 1
			keys.append(switch)
			parseTax[num] = switch
			data[index] = str(parseTax[num])

	with open('parsed.txt', 'w') as t:
		t.write('\n'.join(data))
		t.write('\n\n\n\n\n')
		# t.write(parseTax)