import numpy as np
import random
import matplotlib.pyplot as plt

import PIL


N = 100000


def NormalizeData(data):
    return (data - np.min(data)) / (np.max(data) - np.min(data))


class GenerativeImage(object):

    def __init__(self, address):

        print("***********\nGeneration by", address, "***********")
        if address[0:2] == '0x':
            address[2:]

        config = {}

        # Seed
        config['seed'] = int(address[:3], 16)
        np.random.seed(config['seed'])
        print("SEED:", config['seed'])

        # SIZE
        config['size_sinusoid_0'] = {'A': int(address[3], 16), 'f': int(
            address[4], 16), 'p': int(address[5], 16)}
        config['size_sinusoid_1'] = {'A': int(address[6], 16), 'f': int(
            address[7], 16), 'p': int(address[8], 16)}
        config['size_sinusoid_2'] = {'A': int(address[9], 16), 'f': int(
            address[10], 16), 'p': int(address[11], 16)}
        config['size_noise'] = {'A': int(address[12], 16), 'u': int(
            address[13], 16), 'std': int(address[14], 16)}

        # Colors    def form_size_pdf(self, start=0, stop=10):

        config['colors'] = {'color1': address[15:21],
                            'color2': address[21:27], 'gradient_factor': int(address[27], 16)}

        # Alpha
        config['alpha_sinusoid_0'] = {'A': int(address[28], 16), 'f': int(
            address[29], 16), 'p': int(address[30], 16)}
        config['alpha_sinusoid_1'] = {'A': int(address[31], 16), 'f': int(
            address[32], 16), 'p': int(address[33], 16)}
        config['alpha_sinusoid_2'] = {'A': int(address[34], 16), 'f': int(
            address[35], 16), 'p': int(address[36], 16)}
        config['alpha_noise'] = {'A': int(address[37], 16), 'u': int(
            address[38], 16), 'std': int(address[39], 16)}

        self.config = config
        self.address = address

    def printConfig(self):
        print(self.config)

    def form_alpha_pdf(self, start=0, stop=10):

        x = np.arange(start, stop, stop/N)
        y = np.zeros(N)

        # Sin 1

        for i in range(3):

            alpha = self.config[f'alpha_sinusoid_{i}']
            print(f"**********\n Alpha Sinusoid Configirations {i} \n {alpha}")

            y += alpha['A'] * np.sin(2*np.pi * alpha['f']/15 * x + alpha['p'])

        noise = self.config['alpha_noise']
        print(f"**********\n Alpha Gaussian Noise Configirations \n {noise}")

        mu, sigma = noise['u']-8, noise['std'] / 15
        # mean and standard deviation
        y += noise['A'] * np.random.normal(mu, sigma, N)

        assert len(x) == N

        return NormalizeData(y)

    def form_size_pdf(self, start=0, stop=10):

        x = np.arange(start, stop, stop/N)
        y = np.zeros(N)

        # Sin 1

        for i in range(3):

            size = self.config[f'size_sinusoid_{i}']
            print(f"**********\n Size Sinusoid Configirations {i} \n {size}")

            y += size['A'] * np.sin(2*np.pi * size['f']/15 * x + size['p'])

        noise = self.config['size_noise']
        print(f"**********\n Size Gaussian Noise Configirations \n {noise}")

        mu, sigma = noise['u']-8, noise['std'] / 15
        # mean and standard deviation
        y += noise['A'] * np.random.normal(mu, sigma, N)

        assert len(x) == N

        return y

    def form_color_gradient(self, start=0, stop=10):

        color1 = self.config['colors']['color1']
        color2 = self.config['colors']['color2']
        color1_RGB = tuple(int(color1[i:i+2], 16) for i in (0, 2, 4))
        color2_RGB = tuple(int(color2[i:i+2], 16) for i in (0, 2, 4))

        gradient_factor = self.config['colors']['gradient_factor']

        print(f"Colors \n *******")
        r, g, b = color1_RGB
        print('\033[{};2;{};{};{}m'.format(38, r, g, b) +
              f"color1: #{color1} = {color1_RGB}" + '\033[0m')
        r, g, b = color2_RGB
        print('\033[{};2;{};{};{}m'.format(38, r, g, b) +
              f"color2: #{color2} = {color2_RGB}" + '\033[0m')
        print(f"gradient_factor: {gradient_factor}")

        x = np.arange(start, stop, stop/N)
        y = []
        for _ in range(N):
            y.append(0 if np.random.randint(0, 15) < max(
                min(12, gradient_factor), 2) else 1)

        print("Experimental:", np.sum(y)/N, "- Theory", 1 - gradient_factor/15)

        assert len(x) == N

        colors = []
        for i in y:
            if i == 1:
                colors.append(f"#{color1}")
            else:
                colors.append(f"#{color2}")

        return colors

    def generatePoints(self, size):
        w, h = size
        x = [np.random.uniform(0, w) for _ in range(N)]
        y = [np.random.uniform(0, h) for _ in range(N)]

        assert len(x) == N
        assert len(y) == N

        return x, y
