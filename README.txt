Python script i use to query for my personal files and summarize essays etc that i save on a text file.

It uses the following:

langchain
pgvector
gpt4all
psycopg2-binary

if you want to run the script first install the pgvector by following the link below:

https://bugbytes.io/posts/vector-databases-pgvector-and-langchain/


next install the dependencies by running 'pip install requirements.txt'

after that download an LLM from gpt4all i use 'orca-2-7b.Q4_0.gguf' it requires 8GB RAM you can use any of the available LLM on gpt4all website,
just be mindful of the required RAM as it will be slow the bigger the LLM you are using.


P.S even though i use an LLM that only needs 8GB RAM it would still take at least 5 minutes to generate a response, but its good enough for me as i am not in a hurry,
and its more of a hubby than a necessity. Just wanted to share :-)

and also make sure to remove double quotes from the text file you wish to summarise or add to the vectordb



