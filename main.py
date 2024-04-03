from turtle import bgcolor
from genimage import *

from panda import DATA
import secrets
import argparse


parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--address', help='Ethereum address to generate image for', required=True)
parser.add_argument('--mask', help='Path to the mask image', required=True)

args = parser.parse_args()

# Now you can access the values of the arguments like this:
address = args.address
mask_path = args.mask


id = secrets.token_hex(20)


g = GenerativeImage(id)

g.printConfig()

a = g.form_alpha_pdf()
print(len(a))

sizes = g.form_size_pdf() * 0.5

c = g.form_color_gradient()


x, y = g.generatePoints((745, 174))

imageMap = []

for i in range(N):
    imageMap.append(DATA[int(x[i])][int(y[i])])

imageMap = NormalizeData(imageMap)

fig = plt.figure(figsize=(13, 4))
ax = fig.add_subplot(111, facecolor='black')

ax.scatter(x, y, s=sizes, color=c, alpha=a * imageMap,
           edgecolors='none')

# set axes range
plt.xlim(0, 745)
plt.ylim(0, 174)
plt.show()
fig.savefig(f'samples/{id}.png')
