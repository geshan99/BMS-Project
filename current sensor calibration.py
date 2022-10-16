from sklearn.linear_model import LinearRegression
import numpy as np
import matplotlib.pyplot as plt

x=np.array([1.12,1.13,1.12,1.15,1.17,1.35,1.39,1.67,1.69,1.63]).reshape((-1,1))
y=np.array([0.66,0.66,0.65,0.9,0.94,1.48,1.88,2.62,2.63,2.61])

model=LinearRegression()
model.fit(x,y)
r_sq = model.score(x, y)
print(f'coefficient of determination{r_sq}')
print(f'intercept:{model.intercept_}')
print(f'slope:{model.coef_[0]}')

y_est=model.coef_*x+model.intercept_
plt.title('Current sensor calibration')
plt.xlabel('sensor value')
plt.ylabel('multimeter reading')
plt.plot(x,y,'o')
plt.plot(x,y_est)
plt.show()
