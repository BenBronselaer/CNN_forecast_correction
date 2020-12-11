#!/usr/bin/env python3


# this is an example how this model would be implemented in operations

from forecast_helper import forecast
import scipy.stats as stats
from forecast_conf import (f_directory , model_directory)

fcast=forecast(f_directory )

#fcast.print_dir()

_,_=fcast.load_forecast()

_ =fcast.correct_forecast(model_directory )

# probability of exceeding a given m/s
# assume distribution is log-normal
m = np.mean(np.log(fcast.mod_correct))
s = np.std(np.log(fcast.mod_correct))
p=[]
for k in [50,100,150,200]:
    p.append(100*(1 - stats.norm(m, s).cdf(np.log(k))))


print('Probability of exceeding 0.5 m/s: ' + str('%.2f' % p[0]) +' %')
print('Probability of exceeding 1 m/s: ' + str('%.2f' % p[1] ) +' %')
print('Probability of exceeding 1.5 m/s: ' + str('%.2f' % p[2] ) +' %')
print('Probability of exceeding 2 m/s: ' + str('%.2f' % p[3] ) +' %')