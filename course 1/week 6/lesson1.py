import pandas as pd
import numpy as np

is_tipped = pd.read_csv('sample100.csv').tip_amount>0
ph = is_tipped.mean() # proportion of ones

s = np.sqrt(ph * (1-ph) / len(is_tipped)) # standard deviation for proportion

# alpha - significance level
# alpha = 0.05 - 95% confidence interval
# confidence interval = 1 - alpha
# for alpha=0.05 sigma~1.95996 (two sigma rule?)
# for proprortion: ph +- sigma * s

from statsmodels.stats.proportion import proportion_confint
conf_int = proportion_confint(sum(is_tipped), len(is_tipped), alpha=0.05)

print('For 100 sample Ph is {}, Standart deviation is {}, Confidence interval is from {} to {}'.format(ph, s, conf_int[0], conf_int[1]))


from statsmodels.stats.proportion import samplesize_confint_proportion
# find sample size to get desired confidence interval length
print(int(np.ceil(samplesize_confint_proportion(is_tipped.mean(), 0.01))))

is_tipped = pd.read_csv('sample10000.csv').tip_amount>0
ph = is_tipped.mean()
s = np.sqrt(ph * (1-ph) / len(is_tipped)) # standard deviation for proportion

conf_int10000 = proportion_confint(sum(is_tipped), len(is_tipped), alpha=0.05)
print('For 10000 sample Ph is {}, Standart deviation is {}, Confidence interval is from {} to {}'.format(ph, s, conf_int10000[0], conf_int10000[1]))



# average taxi trip duratuin
sample100 = pd.read_csv('sample100.csv', parse_dates=[1,2])
sample100.head()
sample100['duration'] = [x.total_seconds() / 60 for x in sample100.tpep_dropoff_datetime - sample100.tpep_pickup_datetime]
m = sample100['duration'].mean()

s = sample100['duration'].std(ddof=1) / np.sqrt(len(sample100['duration']))

from statsmodels.stats.weightstats import _tconfint_generic
conf_int = _tconfint_generic(sample100['duration'].mean(), s, len(sample100['duration']) - 1, 0.05, 'two-sided')

print('For 100 sample mean of trip duration is {}, Standart deviation is {}, Confidence interval is from {} to {}'.format(m, s, conf_int[0], conf_int[1]))

sample10000 = pd.read_csv('sample10000.csv', parse_dates=[1,2])
sample10000['duration'] = [x.total_seconds() / 60 for x in sample10000.tpep_dropoff_datetime - sample10000.tpep_pickup_datetime]
m = sample10000['duration'].mean()

s = sample10000['duration'].std(ddof=1) / np.sqrt(len(sample10000['duration']))

conf_int = _tconfint_generic(sample10000['duration'].mean(), s, len(sample10000['duration']) - 1, 0.05, 'two-sided')

print('For 10000 sample mean of trip duration is {}, Standart deviation is {}, Confidence interval is from {} to {}'.format(m, s, conf_int[0], conf_int[1]))


sample100['duration'].median()

sample10000['duration'].median()

sample10000['duration'][sample10000['duration'] < 120].median()


def get_bootstrap_samples(data, n_samples):
    indices = np.random.randint(0, len(data), (n_samples, len(data)))
    samples = data[indices]
    return samples


def stat_intervals(stat, alpha):
    boundaries = np.percentile(stat, [100 * alpha / 2., 100 * (1 - alpha / 2.)])
    return boundaries

median_duration = list(map(np.median, get_bootstrap_samples(sample100['duration'].values, 1000)))

stat_int = stat_intervals(median_duration, 0.05)
print('For 100 sample Confidence interval is from {} to {}'.format(stat_int[0], stat_int[1]))


median_duration = list(map(np.median, get_bootstrap_samples(sample10000['duration'].values, 1000)))
stat_int = stat_intervals(median_duration, 0.05)
print('For 10000 sample Confidence interval is from {} to {}'.format(stat_int[0], stat_int[1]))

print(sample10000.head())


# question 1
in_cash = sample10000.payment_type==2
ph = in_cash.mean() # proportion of ones
print(sum(in_cash)) # how many passangers paid with cash
print(sample10000.payment_type.value_counts())
#question 2
s = np.sqrt(ph * (1-ph) / len(in_cash)) # standard deviation for proportion

# alpha=0.01 so confidence interval is 99%

conf_int = proportion_confint(sum(in_cash), len(in_cash), alpha=0.01)
print(conf_int)

#question 3 average trip distance in miles
distance = sample10000['trip_distance'].mean()
print(distance)

#question 4 standard deviation on trip distance
s_td = sample10000['trip_distance'].std(ddof=1) / np.sqrt(len(sample10000['trip_distance']))
print(s_td)

# question 5 confidence interval for trip distance
conf_int = _tconfint_generic(sample10000['trip_distance'].mean(), s_td, len(sample10000['trip_distance']) - 1, 0.05, 'two-sided')
print(conf_int)