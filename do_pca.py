from sklearn.decomposition import PCA
import pandas as pd

csv_file = "papers.csv"
df = pd.read_csv(csv_file)
df = df.iloc[:, 1:]  # don't use ids
n_components = 50
pca = PCA(n_components=n_components)
pca.fit(df)
pca_df = pd.DataFrame(pca.transform(df), columns=['PCA%i' % i for i in range(n_components)], index=df.index)
pca_df.to_csv("papers_after_pca.csv")
print(sum(pca.explained_variance_ratio_))