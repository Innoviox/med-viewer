# med-viewer

## Inspiration
The coronavirus pandemic shows that the dissemination of useful, reliable and pertinent articles and papers is difficult but extremely crucial to medical research. 

The medical field is very broad, and we would like users - whether its other medical researchers, doctors, or even the press - to get a good sense of what the current state of the art research is. 

Currently, the medical preprint servers such as [medRxiv](https://www.medrxiv.org/) have simple but barebones interfaces to find the latest and most interesting research papers. We would like to improve upon this system to give researchers and the public a richer interface to find articles.

## What it does
In this project, we would like to introduce a personalized recommendation system for medical research articles, especially for COVID-19 research. 

Users can explore our site and mark interesting articles on the homepage using the favorites button. Then, after marking certain articles of interest, the user may visit the recommendations page to simulate the arrival of new articles. These new recommendations would suggest similar and relevant papers, selected from a large pool of articles. 

These news recommendations are dynamic and are based on two machine learning algorithms: TF-IDF and SVM. Periodically, the server will retrain each individual’s recommendation model to reflect the individual’s new favorites and preferences.


## How we built it

We started out by working with the medRxiv site, a medical-preprint server, to query article metadata and PDFs. We built a system to automate the downloads of these files and convert these research articles (PDF) to text files to process downstream. 

Next, we worked on a system to convert the research articles, in text form, into a vector. This algorithm, TF-IDF, creates a content vector of a document, which provides a compressed summary of the articles using the frequency of words. By converting text into a numerical vector, we can run standard machine learning algorithms on these new features. 

Then, for each user, we trained a Support Vector Machine (SVM) classifier based on the user’s favorite articles to predict and suggest new potential “favorites” to the user. The SVM classifier uses a TF-IDF representation of each article to make a prediction, and outputs the probability of an article being a potential “favorite”. 

We created a simple frontend to expose our content recommendation system to the end-user. This frontend includes a flask server, which initiates the training and also the evaluations of SVMs. For our database, we used AirTable as a simple table database. When the user selects their favorites, these articles are added to the user's corresponding row in the AirTable. When the user requests for recommendations, we retrain the user model and generate new results using the SVM.

## Challenges we ran into

We ran into many challenges that we had not anticipated. 

In the beginning, we had difficulty working with the medRxiv api and the extraction of PDFs from the site. We put together a temporary solution, which involved scraping the medRxiv site for a preliminary corpus of PDFs. We learned a lot about using BeautifulSoup and made good use of the Python requests library. We obtained a total of 400 PDFs into total for the final prototype.

We also ran into many issues with setting up the TF-IDF and SVM system. At first, we did not clean the PDF-to-text files to remove numerical tables and other unicode symbols. This caused our vectorizer to include tokens that were not English words, but rather, numbers and floats. Since these characters don’t carry any semantic meaning, we removed these symbols to prevent them from skewing our content vectors. We solved this by integrating a Regular Expression to filter out non alphabetical characters.

For the SVM, we had trouble integrating our database with the vector dimensions it requires. To solve this problem, we had to create a pipeline to effectively translate to and from the models input and outputs. We also had to tweak the SVM several times. One parameter we set was content weighting. Since there are way less favorites than non-favorites in our dataset, we had to make sure that the favorites are given more weight in the model. Before the adjustment, our model would never mark any item as a favorite in our testing dataset. 

## Accomplishments that we're proud of

We are proud of integrating our machine learning models with a frontend. Zach and Rajen, more familiar with data science, learned a lot about Flask and front-end development. Simon, who developed the Flask backend, learned about the various machine learning models used in content recommendation. Together as a team, we were able to deliver a working type that can be presented to an end user. This project required a lot of effective communication and collaboration - we extensively used GitHub branches to share code and datasets. Overall, we had a great experience working together and learned a lot as a team. 
## What's next for Med Viewer

We would like to add the following features:

#### Comments
Comments for different research papers can liven up the database with discussions, but also be used to identify trending articles. Articles with a high engagement factor can be given preference over other articles. 

#### Collaborative Filtering
So far, we only made our recommendations based on each user’s preferences - that is a form of content-based filtering. With collaborative filtering, we not only look at each user’s preferences, but also other similar user’s. This allows us to “cross-recommend” between different users, which allows for more novel and meaningful recommendations.
