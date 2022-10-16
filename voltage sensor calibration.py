from sklearn.linear_model import LinearRegression
import numpy as np
import matplotlib.pyplot as plt
#collected data
x=np.array([2.01,1.96,1.91,1.86,1.87,1.82,1.81,0.72,0.74,0.7,0.71,0.69,0.68,0.67,0.65,0.19]).reshape((-1,1))
y=np.array([10.14,9.88,9.64,9.4,9.4,9.17,9.13,3.68,3.79,3.59,3.59,3.51,3.49,3.4,3.32,1])
#determining the linear regression model
model=LinearRegression()
model.fit(x,y)
r_sq=model.score(x,y)
print(f'coefficient of determination:{r_sq}')
print(f'Intercept:{model.intercept_}')
print(f'slope:{model.coef_[0]}')
#estimating new y values with the model
y_est=model.coef_[0]*x+model.intercept_
#ploting data
plt.title('Voltage sensor calibration')
plt.xlabel('sensor value')
plt.ylabel('voltmeter reading')
plt.plot(x,y,'o')
plt.plot(x,y_est)
plt.show()

