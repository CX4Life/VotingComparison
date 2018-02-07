#Voting Comparison Project
_Comparing the voting pattern of citizens to their Congressional Representative_

###Bird's Eye View
- Scrape the [Congress.gov](https://www.congress.gov/roll-call-votes) listing of role call votes in the US House of Representatives
and the Senate between now and *2008 (subject to change)*
- Grab the voting history of Congressional districts for the same period of time from the
[OpenElections](openelections.net) project.
- Map the Congressional Districts in the OpenElections data to the representatives in the
Congrress.gov data
- Use the [Google Natural Language API](https://cloud.google.com/natural-language/) to perform
sentiment analysis and categorization on the text of ballot measures for both citizens
and representatives
- Model representatives and Congressional districts as an aggregate of their voting for
or against those sentiments
- Evaluate the similarity between Congressional district and its representative


###History

- 2-7-2018 At the suggestion of Dr. Hearne, looking to find some
subset of census data to use to build up a profile of citizens in a
congressional district.

Inserted Representatives into the Representatives MySQL table.

- 2-3-2018 Reviewed the OpenElections data, and discovered
that the amount of data on ballot measures would be insufficient
to perform a large scale analysis on the sentiments of voting
precincts based on sentiment analysis of those ballot measure.
We resolve to perform that same sentiment analysis on the
the text of matters before Congress to create a profile of
each Congressperson, and further use Census data to create a profile of
that Congressperson's constituents. We will use these profiles to
perform outlier detection on the interaction between Congresspeople and
their constituents.

- 1-27-2018 Initial Commit