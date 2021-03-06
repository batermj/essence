import numpy as np
from .module import Module

class Activate(Module):
    def __init__(self, _, inp_shape):
        self.activation = None
        self._out_shape = inp_shape

    def forward(self, x):
        self.transform(x)
        return self.activation

class tanh(Activate):
    def transform(self, x):
        self.activation = np.tanh(x)
    
    def backward(self, grad):
        a = self.activation
        p = 1 - np.multiply(a, a)
        return np.multiply(grad, p)

class softplus(Activate):
    def transform(self, x):
        self.activation = np.log(1 + np.exp(-x))
    
    def backward(self, grad):
        a = self.activation
        p = 1 - np.exp(-a)
        return np.multiply(grad, p)

class sigmoid(Activate):
    def transform(self, x):
        self.activation = 1. / (1. + np.exp(-x))

    def backward(self, grad):
        a = self.activation
        p = np.multiply(a, 1. - a)
        return np.multiply(grad, p)


class linear(Activate):
    def transform(self, x):
        self.activation = x

    def backward(self, grad):
        return grad


class relu(Activate):
    def transform(self, x):
        self.activation = x * (x > 0.)

    def backward(self, grad):
        p = self.activation > 0.
        return np.multiply(grad, p)


class softmax(Activate):
    def transform(self, x):
        row_max = x.max(1, keepdims = True)
        e_x = np.exp(x - row_max)
        e_sum = e_x.sum(1, keepdims = True)
        self.activation = np.divide(e_x, e_sum)

    def backward(self, grad):
        a = self.activation
        m = np.multiply(grad, a)
        g = grad - m.sum(1, keepdims = True)
        return np.multiply(g, a)

class hard_sigmoid(Activate):
    def transform(self, x):
        self.activation = np.clip(
            x * .2 + .5, 0., 1.)
    
    def backward(self, grad):
        a = self.activation
        mask = (a > 0.) * (a < 1.)
        return grad * mask * .2


activation_dict = {
    'tanh': tanh,
    'softplus': softplus,
    'softmax': softmax,
    'linear': linear,
    'relu': relu,
    'sigmoid': sigmoid,
    'hard_sigmoid': hard_sigmoid,
}