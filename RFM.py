import pandas as pd
import datetime


# Arguments (x = value, p = recency, monetary_value, frequency, k = quartiles dict)
def RClass(x, p, d):
    if x <= d[p][0.25]:
        return 1
    elif x <= d[p][0.50]:
        return 2
    elif x <= d[p][0.75]:
        return 3
    else:
        return 4


# Arguments (x = value, p = recency, monetary_value, frequency, k = quartiles dict)
def FMClass(x, p, d):
    if x <= d[p][0.25]:
        return 4
    elif x <= d[p][0.50]:
        return 3
    elif x <= d[p][0.75]:
        return 2
    else:
        return 1


def df_print(df):
    print(df.to_markdown(tablefmt="fancy_grid"))


df_data = pd.read_csv('RFM201810.csv', low_memory=False)

# print(df_data.columns)
df_data['InvoiceDate'] = pd.to_datetime(df_data['InvoiceDate'])
last_date = df_data['InvoiceDate'].max()

rfmTable = df_data.groupby('CustomerCode').agg({'InvoiceDate': lambda x: (last_date - x.max()).days,
                                                'InvoiceNo': lambda x: len(x),
                                                'Amount': lambda x: x.sum()})
# print(rfmTable.InvoiceNo.max())

rfmTable['InvoiceDate'] = rfmTable['InvoiceDate'].astype(int)
rfmTable.rename(columns={'InvoiceDate': 'recency',
                         'InvoiceNo': 'frequency',
                         'Amount': 'monetary_value'}, inplace=True)

quantiles = rfmTable.quantile(q=[0.25,0.5,0.75])
rfmSegmentation = rfmTable

rfmSegmentation['R_Quartile'] = rfmSegmentation['recency'].apply(RClass, args=('recency',quantiles,))
rfmSegmentation['F_Quartile'] = rfmSegmentation['frequency'].apply(FMClass, args=('frequency',quantiles,))
rfmSegmentation['M_Quartile'] = rfmSegmentation['monetary_value'].apply(FMClass, args=('monetary_value',quantiles,))

rfmSegmentation['RFMClass'] = rfmSegmentation.R_Quartile.map(str) \
                            + rfmSegmentation.F_Quartile.map(str) \
                            + rfmSegmentation.M_Quartile.map(str)

print(len(rfmSegmentation['RFMClass'].loc[rfmSegmentation['RFMClass'] == '111']))
# df_print(rfmSegmentation[:2])
# df_data.info()
