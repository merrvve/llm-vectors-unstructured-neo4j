import os
from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI
from langchain_community.graphs import Neo4jGraph
llm = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

response = llm.embeddings.create(
        input="Text to create embeddings for",
        model="text-embedding-ada-002"
    )

embedding = response.data[0].embedding


#tag::connect[]
graph = Neo4jGraph(
    url=os.getenv('NEO4J_URI'),
    username=os.getenv('NEO4J_USERNAME'),
    password=os.getenv('NEO4J_PASSWORD')
)
#end::connect[]

#tag::query[]
result = graph.query("""
CALL db.index.vector.queryNodes('chunkVector', 6, $embedding)
YIELD node, score
RETURN node.text, score
""", {"embedding": embedding})
#end::query[]

#tag::print[]
for row in result:
    print(row['node.text'], row['score'])
#end::print[]