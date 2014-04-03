# Copyright 2013, 2014 Justis Grant Peters and Sagar Jauhari

# This file is part of BCIpy.
# 
# BCIpy is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# BCIpy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with BCIpy.  If not, see <http://www.gnu.org/licenses/>.

#==============================================================================
# Random Forest Classifier
#    Bib: [Breiman, Leo. "Random forests." Machine learning 45.1 (2001): 5-32.]
#    Brief overview: http://blog.yhathq.com/posts/random-forests-in-python.html
# This classifier is often as the first technique to find out obvious and 
# sometimes not-so-obvious relationships
#==============================================================================
subj_id = 27

df = pd.DataFrame({'att':[int(i[2]) for i in cln_data[subj_id]],
                    'med':[int(i[3]) for i in cln_data[subj_id]],
                    'difficulty':[int(i[4]) for i in cln_data[subj_id]]})
df['is_train'] = np.random.uniform(0, 1, len(df)) <= .75
df.head()

from sklearn.metrics import classification_report

train, test = df[df['is_train']==True], df[df['is_train']==False]
features = df.columns[[0,2]]

clf = RandomForestClassifier(n_jobs=2)
clf.fit(train[features], train['difficulty'])

preds = clf.predict(test[features])

print classification_report(test['difficulty'], preds)
pd.crosstab(test['difficulty'], preds, rownames=['actual'], colnames=['preds'])
