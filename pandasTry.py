# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# In[34]:


print(1.)
print("Series")
print(pd.Series(1,index=list(range(6)),dtype='float32'),"\n")
print("Timestamp")
print(pd.Timestamp('20130102'), "\n")
print("array")
print(np.array([3] * 6,dtype='int32'), "\n")
print("pd.Categorical")
print(pd.Categorical(["test","train","test","train"]), "\n")

df2 = pd.DataFrame({ 'A' : 1.,
                      'B' : pd.Timestamp('20130102'),
                      'C' : pd.Series(1,index=list(range(6)),dtype='float32'),
                      'D' : np.array([3] * 6,dtype='int32'),
                      'E' : pd.Categorical(["test","train","test",np.nan,"test","train"]),
                      'F' : 'foo' })
print(df2.head(7))
print(df2.dtypes)
print("df2's index\n",df2.index)
print("df2's columns\n", df2.columns)
print("df2's values\n", df2.values)
print("df2's summary describe\n", df2.describe())
print("df2's transpose\n", df2.T)


# In[152]:


dates = pd.date_range('20130101', periods=6)
df = pd.DataFrame(np.random.randn(6,4), index=dates, columns=list('ABCD'))
print("df : \n", df)
print("df sorted by B : \n", df.sort_values(by="B"))
print("df['A']*3 : \n", df['A']*3)
#print("df[0:3] : \n", df.loc[['2013-01-02','2013-01-04'],['A','C']])
print("df.iloc[:,0:3] : \n", df.iloc[:,0:3])
df3 = df
df3 = df3.iloc[:,0:3]
df3.loc[:,'E'] = ['one', 'one','two','three','four','three']
df3['F'] = np.array([5] * len(df))
df3 = df3.reindex( columns=list(df3.columns) + ['G'])
df3.iloc[0:2,len(df3)-1] = 1
print("df3 : \n", df3)
print("df3 group by E & A &B : \n", df3.groupby(['E','A','B']).sum())
print("df3 stack() : \n", df3.stack())
print("df : \n", df.apply(lambda x: x.max() - x.min()))
print("df : \n", df)
print("df.A : \n", df.A)
print("df.A > 0 : \n", df.A > 0)
print("df[[True,False,False,False,False,True]] : \n",
      df[[True,False,False,False,False,True]])


# In[121]:


a = [1,3,5]
b = a#.copy()
b.append(7)
b = b + [11,13]
a.append(9)
print("a : \n", a)
print("b : \n", b)


# In[144]:


_mask = df3.index.isin(['20130101', '20130104'])
print(df3[_mask])


# In[164]:


df4 = pd.DataFrame({'A' : ['one', 'one', 'two', 'three'] * 3,
                   'B' : ['A', 'B', 'C'] * 4,
                   'C' : ['foo', 'foo', 'foo', 'bar', 'bar', 'bar'] * 2,
                   'D' : np.random.randn(12),
                   'E' : np.random.randn(12)})
print(" df4 : \n", df4)
pivotTable = pd.pivot_table(df4,
                            values='D',
                            index=['A','B'],
                            columns=['C'])
print(" pivot table : \n", pivotTable)

pivotTable.to_csv('foo.csv',
          index=False)
iris = pd.read_csv('iris.csv')
print(' iris : \n',iris)


# In[ ]:




