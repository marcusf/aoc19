import utils, interp

stream = utils.read_input(fname='05.input')
output, mapping = interp.parse(stream)
a, b, _ = interp.run(stream, data_input=[5], debug=True)
print(b)


