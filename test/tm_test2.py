from random import seed
from random import random, randint, gauss, uniform
from matplotlib import pyplot

# # Sample
# seed(3)
# random_walk = list()
# random_walk.append(-1 if random() < 0.5 else 1)     # random() generates random number between 0 and 1
# for i in range(1, 1000):
#     movement = -1 if random() < 0.5 else 1
#     value = random_walk[i-1] + movement
#     random_walk.append(value)
# pyplot.plot(random_walk)
# pyplot.show()

# Temperaturverlauf


# # Sollkurve
# mean = 4
# sigma = 20
# seed_nr = randint(1, 1000)
# start_value = 0
# start_time = 0
# interval1_end = start_time + randint(500, 600)     # Rise
# interval2_end = interval1_end + randint(500, 600)      # Fall
#
# seed(seed_nr)
# random_walk = list()
# random_walk.append(start_value)     # random() generates random number between 0 and 1
# for i in range(1, interval2_end):
#     # movement = -1 if random() < 0.5 else 1
#     movement = abs(gauss(mean, sigma))
#     if i < interval1_end:
#         value = random_walk[i - 1] + movement
#     else:
#         value = random_walk[i - 1] - movement
#     random_walk.append(value)
# pyplot.plot(random_walk)
# pyplot.show()

# Kraftverlauf sklearn, np.polyfit
from sklearn.linear_model import LinearRegression
import numpy as np
import matplotlib.pyplot as plt

# x = np.random.randn(10, 1)
# y = 2*x**2+3+0.1*np.random.randn(10, 1)
#
# plt.scatter(x, y)
# plt.show()
#
# model = LinearRegression()
# model.fit(x, y)
#
# print("model.coef_ = {}".format(model.coef_))
#
# print("model.predict = {}".format(model.predict(40)))
#
# x_test = np.linspace(-3, 3)
# y_pred = model.predict((x_test[:,None]))
#
# plt.scatter(x, y)
# plt.plot(x_test, y_pred, 'r')
# plt.legend(['Predicted line', 'Observed data'])
# plt.show()


num_points = 10
length_time_series_ms = 1000 + uniform(-50, 50)      # Length of time series
dev_time = 200       # deviation on time axis
dev_value = 10       # deviation on values axis

x_soll = list(range(0, 1000, 100))
y_soll = [0, 5, 20, 30, 40, 45, 20, 10, 7, 4]

x_val_ist = []
y_val_ist = []

# plt.scatter(x_soll, y_soll)
# plt.show()

for index, value in enumerate(x_soll):
    pass
    if index == 1:
        x_val_ist.append(0)
        y_val_ist.append(0)
    else:
        x_val_ist.append(value + uniform(-dev_time, dev_time))
        y_val_ist.append(y_soll[index] + uniform(-dev_value, dev_value))


fit_soll = np.poly1d(np.polyfit(x_soll, y_soll, 4))
fit_ist = np.poly1d(np.polyfit(x_val_ist, y_val_ist, 4))

print('fit_soll(range(0,4) = {}'.format(fit_soll(range(0,4))))

xp = np.linspace(0, 900, 10)

fig = plt.figure()
ax1 = fig.add_subplot(111)
ax1.plot(x_val_ist, y_val_ist, '.r', x_soll, y_soll, '.g', xp, fit_ist(xp), '-r', xp, fit_soll(xp), '-g')

# ax1.scatter(x_val_ist, y_val_ist)
# ax1.scatter(x_soll, y_soll)
#
# ax1.plot(xp, fit_soll(xp), '--')

plt.show()


# x = np.array([0.0, 1.0, 2.0, 3.0,  4.0,  5.0])
# y = np.array([0.0, 0.8, 0.9, 0.1, -0.8, -1.0])
# z = np.polyfit(x, y, 3)
#
# p = np.poly1d(z)
# p30 = np.poly1d(np.polyfit(x, y, 30))
#
# xp = np.linspace(-2, 6, 100)
# _ = plt.plot(x, y, '.', xp, p(xp), '-', xp, p30(xp), '--')
# plt.ylim(-2,2)
# plt.show()





import numpy as np
import matplotlib.pyplot as plt


x = x_soll # np.arange(0, 2*np.pi+np.pi/4, 2*np.pi/8)
y = y_soll # np.sin(x)

plt.figure()
plt.plot(x, y, 'r')
plt.legend(['Linear', 'Cubic Spline', 'True'])
plt.axis([-0.05, 1000, 0, 60])
plt.title('Cubic-spline interpolation')
plt.show()





