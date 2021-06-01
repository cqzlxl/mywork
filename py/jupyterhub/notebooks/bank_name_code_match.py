#!/usr/bin/env python
# coding: utf-8

# In[1]:


import logging

import jieba
import joblib
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.feature_extraction.text import TfidfVectorizer


# In[2]:


logging.basicConfig(
    format="%(asctime)s %(levelname)s %(name)s %(processName)s.%(threadName)s[%(process)d.%(thread)d]: %(message)s",
    level=logging.DEBUG,
)

logs = logging.getLogger(__name__)


# In[3]:


class NameCodeMatcher(TransformerMixin, BaseEstimator):
    @staticmethod
    def tokenize(text):
        return jieba.cut(text, cut_all=True)

    def __init__(self, topk=4, name_tokenizer=None):
        self.name_tokenizer = name_tokenizer
        self.topk = topk
        self.calc = list()

    def fit(self, X, y):
        vectorizer = TfidfVectorizer(tokenizer=self.name_tokenizer or self.tokenize).fit(X)
        for prefix in y.str.slice(0, 3).unique():
            part = y.str.startswith(prefix)
            name = X[part]
            code = y[part]
            logs.info("try to fit banks part %s, %d samples", prefix, len(name))
            calc = NameSimilarityCalc(prefix, vectorizer, self.topk)
            calc.fit(name, code)
            self.calc.append(calc)
            logs.info("done fitting banks part %s", prefix)
        return self

    def transform(self, X):
        return pd.concat(
            pd.concat(c.transform([q]) for c in self.calc).nsmallest(self.topk, "similarity") for q in X
        ).drop(columns="part")[["code", "name", "similarity"]].reset_index(drop=True)

    def vectorize(self, X):
        return self.calc[0].vectorize(X)

    def match(self, X):
        return self.transform(X)


class NameSimilarityCalc(TransformerMixin, BaseEstimator):
    @staticmethod
    def l2_norm(vects):
        return np.sqrt((vects * vects.T).sum(axis=1))

    def __init__(self, part, vectorizer, topk=256):
        self.vectorizer = vectorizer
        self.part = part
        self.topk = topk
        self.sample_names = None
        self.sample_codes = None
        self.sample_vects = None
        self.sample_norms = None

    def fit(self, X, y):
        df = pd.DataFrame(dict(name=X, code=y)).reset_index(drop=True)
        X, y = df.name, df.code
        self.sample_names = X
        self.sample_codes = y
        self.sample_vects = self.vectorizer.transform(X).T
        self.sample_norms = self.l2_norm(self.sample_vects.T).T
        return self

    def transform(self, X):
        vects = self.vectorize(X)
        norms = self.l2_norm(vects)
        v = vects * self.sample_vects
        n = norms * self.sample_norms
        d = 1 - v / n            
        return pd.concat(self.rank(d, X))

    def rank(self, distances, queries):
        index = distances.argsort(axis=1).A[:, :self.topk]
        for i, d, q in zip(index, distances.A, queries):
            name = self.sample_names[i]
            code = self.sample_codes[i]
            yield pd.DataFrame(dict(part=self.part, name=name, code=code, similarity=d[i], query=q))

    def vectorize(self, words):
        return self.vectorizer.transform(words)


# In[4]:


train_path = "./banks.csv"
model_path = "./model.dat"

df = pd.read_csv(
    train_path,
    engine="python", encoding="gbk", sep=r"|",
    usecols=[0, 1, 12], names=["code", "status", "name"], dtype=dict(code=str, status=bool, name=str)
)

df = df[df.status].drop(columns="status")


# In[5]:


queries = ["建行顺义", "建行木樨地"]
matcher = NameCodeMatcher(topk=8)
matcher.fit(df.name, df.code)
matcher.match(queries)


# In[6]:


joblib.dump(matcher, model_path)


# In[7]:


m = matcher.vectorize(["新韩银行（中国）有限公司北京顺义支行", "中国工商银行"])
v = matcher.vectorize(["北京顺义"])


# In[8]:


model = joblib.load(model_path)
model.match(queries)
