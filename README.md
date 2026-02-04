# Computing the Geographical Center of US Presidents' Speeches
> Eric Gutiérrez, 2nd February 2026.

### The Story
In almost any speech, political leaders mention places, in both friendly and unfriendly ways. By retrieving the names of the places a given political figure uses in speeches, we can derive a comprehensible spatial pattern, which will likely be strongly tied to his or her policies and stances on several issues. In this project, we use 1,000+ speeches from US Presidents to generate a spatial pattern for each President. In addition, we provide a measure of the _geographical center_ of each US President in history.

### Data & Methods
The Miller Center of Public Affairs, University of Virginia, has a rich database with more than a thousand Presidential speeches, which we use in this project.

> [!NOTE]Data Source
> Miller Center of Public Affairs, University of Virginia. "_Presidential Speeches: Downloadable Data._" Accessed January 31, 2026. [data.millercenter.org](data.millercenter.org).

First, we combine the speeches, which come in separate `json` files, in a single `csv` file. Once this is done, we proceed in retrieving the names of the places present in each speech. To do so, we use the Natural Language Processing (NLP) library `spacy`, which has the ability to label the words in a text, including geopolitical entities and locations. As a result, we obtain a list of the places in a given speech, along with how many times a place was mentioned, a list of unique places, and the number of unique places mentioned.

The next step involves obtaining the coordinates for each unique place retrieved in the previous step, using the `geopy` library. As a result, we generate a table that contains the latitude and longitude in WGS84 for each unique place. Next, we join the coordinates with the places identified in each speech. The resulting table resembles the following structure:

|title | date | president | place | num_places | lat | long |
|----------|----------|----------|----------|----------|----------|----------|
| February 27, 1860: Cooper Union Address | 1860-02-27T13:03:58-04:56 | Abraham Lincoln | 3 | Country | | |
| February 27, 1860: Cooper Union Address | 1860-02-27T13:03:58-04:56 | Abraham Lincoln | 3 | Country | | |
| February 27, 1860: Cooper Union Address | 1860-02-27T13:03:58-04:56 | Abraham Lincoln | 3 | Country | | |
| February 27, 1860: Cooper Union Address | 1860-02-27T13:03:58-04:56 | Abraham Lincoln | 3 | Country | | |
| ... | ... | ... | ... | ... | ... | ... |

To compute the geographical center of each US President, a metodological decision must be made regarding how will the aggregation of the places' coordiantes take place. To find the centroids on a shpere, we must first convert the coordinates to 3D Cartesian vectors, average them in that space, and convert them back. However, the decision has to do with how to deal with the fact that some places are mentioned more than once in a speech. One option is to use the unique places mentioned, and thus for each place to enter the average only once, without consideration for how many times they have been repeated. We consider that this approach can distort the results, provided that usual terms such as "_America_" or "_the United States_" will be pressumably severely underrepresented. In addition, this approach would require for places with different names or expressed in different manners, such as "_the United States_" and "_the US_", to be grouped together.

Another alternative option is for each place to enter the average each time that it has been mentioned. This not only solves the problem of misrepresentation mentioned above, but it also makes unnecessary further data preprocessing to group together different terms that refer to a common place. Although this approach is nonetheless sensible to the realtive number of times that a place appears in a speech, we have selected it provided that is the most sensible of the two options in hand.

At the moment, all the coordinates of all the places mentioned on a speech have the same weight whem computing the center. However, the code allows for this weights to be set in a different manner if needed.

### Results

### Conclusions