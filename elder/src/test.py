import matplotlib.pyplot as plt

plt.ion()
plt.plot([1.6, 2.7])

plt.title("interactive test")
plt.xlabel("index")
plt.pause(0.1)

plt.plot([1.5,3.5])

plt.draw()

plt.pause(0.1)