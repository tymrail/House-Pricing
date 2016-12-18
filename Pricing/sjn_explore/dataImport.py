__author__ = 'cat'
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np

def read_train(file_path):
    data = pd.read_csv(file_path, index_col=False)

    data.drop(['Street', 'Utilities', 'Condition2', 'RoofMatl', 'Alley',
               'GarageYrBlt', 'GarageCond', 'PoolQC', 'MiscFeature'],
              axis=1, inplace=True)

    # marked as NA in BsmtExposure and not NA in other Bsmt Attributes
    data.loc[np.logical_xor(data['BsmtCond'].isnull(), data['BsmtExposure'].isnull()), 'BsmtExposure'] = 'No'

    # LotFrontage's N/A is assigned zero, will it cause problem?
    data.fillna(value={'MasVnrType': 'None', 'MasVnrArea': 0, 'BsmtQual': 'NoBsmt', 'BsmtCond': 'NoBsmt',
                       'BsmtExposure': 'NoBsmt', 'BsmtFinType1': 'NoBsmt', 'BsmtFinType2': 'NoBsmt',
                       'Electrical': 'SBrkr', 'FireplaceQu': 'NoFP', 'GarageType': 'Noga',
                       'GarageFinish': 'Noga', 'GarageQual': 'Noga', 'Fence': 'NoFence', 'LotFrontage': 0},
                inplace=True)

    data.loc[:, 'YrSold'] = 2016 - data.loc[:, 'YrSold']

    data.loc[data.loc[:, 'PoolArea'] != 0, 'PoolArea'] = 1

    data.loc[:, 'Porch'] = np.sum(data.loc[:, ['EnclosedPorch', '3SsnPorch', 'ScreenPorch']], axis=1)
    data.drop(['EnclosedPorch', '3SsnPorch', 'ScreenPorch'], axis=1, inplace=True)

    data.replace({'BsmtFullBath': {3: 2}, 'LotShape': {'IR3': 'IR2'}}, inplace=True)

    return data

def na_cols(df):
    # examine columns containing NA value
    na_col = df.columns[np.sum(df.isnull(), axis=0) != 0]
    print 'columns containing NA are {}'.format(na_col)
    return na_col
