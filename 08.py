import utils

def pick_color(i, layers):
    for layer in layers:
        if layer[i] == 1 or layer[i] == 0:
            return layer[i]
    return 2

image=utils.read_input(delim=None)
WIDTH = 25
HEIGHT = 6
LAYER_SIZE=WIDTH*HEIGHT

layers = list()

for i in range(round(len(image)/LAYER_SIZE)):
    layers.append(image[i*LAYER_SIZE:(i+1)*LAYER_SIZE])

# To make sure the image wasn't corrupted during transmission, the Elves would like you to find the layer 
# that contains the fewest 0 digits. On that layer, what is the number of 1 digits multiplied by the number of 2 digits?
weights  = [sum([1 if x == 0 else 0 for x in layer]) for layer in layers]
minn = weights.index(min(weights))

minlayer = layers[minn]

ones = sum([1 if x == 1 else 0 for x in minlayer])
twos = sum([1 if x == 2 else 0 for x in minlayer])
print(ones*twos)

image = [pick_color(i, layers) for i in range(WIDTH*HEIGHT)]

for i in range(HEIGHT):
    row = image[i*WIDTH:(i+1)*WIDTH]
    print(''.join([' ' if r == 0 else '#' for r in row]))
