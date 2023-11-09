import matplotlib
matplotlib.use('Qt5Agg')
import itertools
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.stats.api as sms
from scipy.stats import ttest_1samp, shapiro, levene, ttest_ind, mannwhitneyu, \
    pearsonr, spearmanr, kendalltau, f_oneway, kruskal
from statsmodels.stats.proportion import proportions_ztest

# Megabook kısa süre önce mevcut "maximum bidding" adı verilen teklif verme türüne alternatif olarak
# yeni bir teklif türü olan "average bidding"’i tanıttı.


# Impression: Reklam görüntüleme sayısı
# Click: Görüntülenen reklama tıklama sayısı
# Purchase: Tıklanan reklamlar sonrası satın alınan ürün sayısı
# Earning: Satın alınan ürünler sonrası elde edilen kazanç


pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 10)
pd.set_option('display.float_format', lambda x: '%.5f' % x)



# Adım 1: ab_testing_data.xlsx adlı kontrol ve test grubu verilerinden oluşan veri setini okutunuz.
# Kontrol ve test grubu verilerini ayrı değişkenlere atayınız
#*************************************************

maximum_bidding = pd.read_excel("ab_testing.xlsx",sheet_name="Control Group")
maximum_bidding.head()
average_bidding = pd.read_excel("ab_testing.xlsx",sheet_name="Test Group")
average_bidding.head()


# Adım 2: Kontrol ve test grubu verilerini analiz ediniz.

maximum_bidding.describe()

"""ÇIKTI 
    Impression      Click  Purchase    Earning
count     40.00000   40.00000  40.00000   40.00000
mean  101711.44907 5100.65737 550.89406 1908.56830
std    20302.15786 1329.98550 134.10820  302.91778
min    45475.94296 2189.75316 267.02894 1253.98952
25%    85726.69035 4124.30413 470.09553 1685.84720
50%    99790.70108 5001.22060 531.20631 1975.16052
75%   115212.81654 5923.80360 637.95709 2119.80278
max   147539.33633 7959.12507 801.79502 2497.29522
"""

average_bidding.describe()

"""ÇIKTI
     Impression      Click  Purchase    Earning
count     40.00000   40.00000  40.00000   40.00000
mean  120512.41176 3967.54976 582.10610 2514.89073
std    18807.44871  923.09507 161.15251  282.73085
min    79033.83492 1836.62986 311.62952 1939.61124
25%   112691.97077 3376.81902 444.62683 2280.53743
50%   119291.30077 3931.35980 551.35573 2544.66611
75%   132050.57893 4660.49791 699.86236 2761.54540
max   158605.92048 6019.69508 889.91046 3171.48971
"""

maximum_bidding.info()

plt.hist(maximum_bidding["Purchase"])
plt.show()
# Figure_1.png

plt.hist(average_bidding["Purchase"])
plt.show()
# Figure_2.png


#------------------------------------------------------

# Adım 1: Hipotezi tanımlayınız.

# H0 : M1 = M2  maximum bidding ile average bidding ortalamaları arasında fark yoktur
# H1 : M1!= M2 ... fark vardır


# Adım 2: Kontrol ve test grubu için purchase (kazanç) ortalamalarını analiz ediniz

maximum_bidding["Purchase"].mean()
#550.8940587702316
average_bidding["Purchase"].mean()
#582.1060966484677

# Adım 1: Hipotez testi yapılmadan önce varsayım kontrollerini yapınız.
# Bunlar Normallik Varsayımı ve Varyans Homojenliğidir. Kontrol ve test grubunun normallik varsayımına uyup uymadığını Purchase değişkeni
# üzerinden ayrı ayrı test ediniz.

  # Normallik Varsayımı :
  # H0: Normal dağılım varsayımı sağlanmaktadır.
  # H1: Normal dağılım varsayımı sağlanmamaktadır.
  # p < 0.05 H0 RED , p > 0.05 H0 REDDEDİLEMEZ
  # Test sonucuna göre normallik varsayımı kontrol ve test grupları için sağlanıyor mu ? Elde edilen p-value değerlerini yorumlayınız.

test_stat, pvalue = shapiro(maximum_bidding[ "Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))
#Test Stat = 0.9773, p-value = 0.5891

test_stat, pvalue = shapiro(average_bidding[ "Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))
#Test Stat = 0.9589, p-value = 0.1541


  # Varyans Homojenliği :
  # H0: Varyanslar homojendir.
  # H1: Varyanslar homojen Değildir.
  # p < 0.05 H0 RED , p > 0.05 H0 REDDEDİLEMEZ
  # Kontrol ve test grubu için varyans homojenliğinin sağlanıp sağlanmadığını Purchase değişkeni üzerinden test ediniz.
  # Test sonucuna göre normallik varsayımı sağlanıyor mu? Elde edilen p-value değerlerini yorumlayınız.

test_stat, pvalue = levene(maximum_bidding[ "Purchase"],
                           average_bidding[ "Purchase"])

print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))
#Test Stat = 2.6393, p-value = 0.1083


# Adım 2: Normallik Varsayımı ve Varyans Homojenliği sonuçlarına göre uygun testi seçiniz.

test_stat, pvalue = ttest_ind(maximum_bidding[ "Purchase"],
                           average_bidding[ "Purchase"],
                              equal_var=True)

print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))
#Test Stat = -0.9416, p-value = 0.3493



# Adım 3: Test sonucunda elde edilen p_value değerini göz önünde bulundurarak kontrol ve test grubu satın alma ortalamaları arasında istatistiki
# olarak anlamlı bir fark olup olmadığını yorumlayınız

#maximum bidding ile average bidding ortalaması arasında istatistiksel olarak fark yoktur



#Adım 1: Hangi testi kullandınız, sebeplerini belirtiniz.

# Parametric test kullandım. Ttest_ind
# Çünkü normallık varsayımına baktığımda pvalue değeri 0.05 den büyük olduğu için H0 reddedilemez çıktı
# ve normal dağılım varsayımı kabul edilmiş oldu bu yüzden parametrik test kullandm.


#Adım 2: Elde ettiğiniz test sonuçlarına göre müşteriye tavsiyede bulununuz

# Elde edilen test sonucuna göre Maximum Bidding,Average Bidding arasında fark yoktur.
# Çalışma süresi uzatılabilir, gözlem sayısını arttırmak için
# Pvalue değerinde oynama yapılabilir
# Purchase değişkeninin yanında diğer değişkenlere de bakılarak bir sonuç çıkarılabilir.

