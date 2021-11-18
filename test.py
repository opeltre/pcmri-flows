from pcmri import Dataset
import torch
import matplotlib.pyplot as plt

db = Dataset('full')
file = db.get("b*")

f = file.read('cig-cervi')

def flows (k, fmt='torch'):
    file = db.get(k)
    x = file.flows(fmt=fmt)
    m = x.mean(dim=[1])
    x = x * torch.sign(m)[:,None]
    x[2] *= (m[0] / m[2]).abs() 
    x[3] *= (m[1] / m[3]).abs()
    x[4] *= torch.sign(torch.dot(x[0], x[4]))
    return x

def plot(k, fmt='torch'):
    x = flows(k, fmt)
    plt.plot(x[0], color='red')
    plt.plot(x[1], color='red', linestyle='dashed')
    plt.plot(x[2], color='blue')
    plt.plot(x[3], color='blue', linestyle='dashed')
    plt.plot(x[0] - x[2], color='purple')
    plt.plot(x[1] - x[3], color='purple', linestyle='dashed')
    plt.plot(x[4], color='green')
    plt.plot(
        torch.zeros(x.shape[1:]), color='grey', linewidth=0.8)
    plt.show()

def plotvol (k, fmt='torch'):
    x = flows(k, fmt)
    vb0 = (x[0] - x[2]).cumsum(0)
    vb1 = (x[1] - x[3]).cumsum(0)
    vcs = (x[4] - x[4].mean()).cumsum(0)
    vi0 = vb0 - vcs
    vi1 = vb1 - vcs
    plt.plot(vb0 - vb0.mean(), color="purple")
    plt.plot(vb1 - vb1.mean(), color="purple", linestyle="dashed")
    plt.plot(vcs - vcs.mean(), color="green")
    plt.plot(vi0 - vi0.mean(), color="orange")
    plt.plot(vi1 - vi1.mean(), color="orange", linestyle="dashed")
    plt.plot(torch.zeros([vb0.shape[0]]), color="grey", linewidth=0.8)
    plt.show()
