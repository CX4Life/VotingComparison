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
- 1-27-2017 Initial Commit