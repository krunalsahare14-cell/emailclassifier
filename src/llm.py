# from haystack import Document, Pipeline
# from haystack_integrations.components.generators.ollama import OllamaGenerator
# from haystack.components.preprocessors import DocumentCleaner
# from haystack.components.builders.prompt_builder import PromptBuilder
# from haystack.components.retrievers.in_memory import InMemoryBM25Retriever
# from haystack.document_stores.in_memory import InMemoryDocumentStore
# from json import loads

# # Load the RAG JSON
# with open('src/data/rag.json', 'r') as f:
#     data = loads(f.read())

# docs = []
# for doc in data['nodes']:
#     docs.append(Document(content=str(doc)))

# # Clean and pre-process the RAG JSON (Optional)
# cleaner = DocumentCleaner()
# ppdocs = cleaner.run(documents=docs)

# # We are using an In-memory Document store for RAG
# docu_store = InMemoryDocumentStore()
# docu_store.write_documents(ppdocs['documents'])

# retriever = InMemoryBM25Retriever(document_store=docu_store, top_k=1)

# template = '''
#     As the person in charge of mail distribution, your task is to direct emails to the right recipients.
#     Use the context provided to determine the most fitting recipient(s) for the query.
#     The context includes the organization's structure, departments, and teams.
#     You can also use the description tag from the context to match the semantic meaning of the email.
#     Your answer should be the id of the team(s) at the leaf node of the hierarchy to whom the query should be directed.
    
#     Context: 
#     {% for document in documents %}
#         {{ document.content }}
#     {% endfor %}
    
#     Query: {{ query }}
#     Please respond in the following format: <x>
#     where 'x' is the id of the leaf node.
#     Your answer should ONLY INCLUDE THE ID
#     '''
    
# prompt_builder = PromptBuilder(template=template)

# # You can use Llama3.1 to provide better responses, but since Qwen 4b is 
# # a smaller and faster model, you can use it on less-powerful hardware as well
# generator = OllamaGenerator(model="qwen:4b",
#                             url = "http://localhost:11434",
#                             generation_kwargs={
#                               "num_predict": 100,
#                               "temperature": 0.1,
#                               },
#                             )

# # Build the RAG pipeline
# rag_pipeline = Pipeline()
# rag_pipeline.add_component("retriever", retriever)
# rag_pipeline.add_component("prompt_builder", prompt_builder)
# rag_pipeline.add_component("llm", generator)
# rag_pipeline.connect("retriever", "prompt_builder.documents")
# rag_pipeline.connect("prompt_builder", "llm")


# def return_ans(query):
#     query="is this email a phishing email? answer in one word  "+query[:5000]
#     try:
#         print("QUERY:", query[:5000])
#         ans = rag_pipeline.run({
#             "prompt_builder": {"query": query[:5000]},
#             "retriever": {"query": query[:5000]}
#         })
#         # print("RAW MODEL OUTPUT:", ans)

#         # If no output returned
#         if not ans:
#             return {"team": "unknown"}

#         llm_data = ans.get("llm", {})
#         # print(f"llm_data,{llm_data}")
#         replies = llm_data.get("replies", [])
#         print(f"replies,{replies}")

#         # If replies is empty
#         if not replies:
#             return {"team": "unknown"}

#         return {"team": replies[0].strip()}

#     except Exception as e:
#         print("ERROR:", e)
#         return {"team": "unknown"}
# # def return_ans(query):
# #     try:
# #         ans = rag_pipeline.run({"prompt_builder": {"query": query},
# # 									"retriever": {"query": query}})
# #         print(ans)
# #         response = {
# #             "team": ans['llm']['replies'][0].strip()
# #         }
# #         return response
# #     except:
# #         response = {
# #             "team": ans['llm']['replies'][0].strip()
# #         }
# #         return response
    
# def test_output():
#     content = '''
#     I am writing to report a specific issue I have been facing with the online banking platform that requires attention and resolution.

# The problem I am encountering revolves around inconsistencies in the transaction history displayed in my online banking account. Specifically, certain transactions appear to be duplicated or missing altogether, leading to confusion and inaccurate financial records.


# For example, on 2nd April, I noticed that a transaction for $5000 appears twice in my transaction history, resulting in an incorrect balance calculation. Furthermore, transactions made on 4th April do not reflect in the transaction history, despite being successfully processed and confirmed by Barclays.


# These discrepancies not only disrupt my ability to track and manage my finances accurately but also raise concerns about the reliability and integrity of the online banking system.


# I urge your technical team to investigate this matter promptly and rectify the issues causing these inconsistencies in the transaction history. It is crucial to ensure that the online banking platform provides accurate and up-to-date information to customers to maintain trust and confidence in Barclays' services.


# I kindly request regular updates on the progress made in resolving this issue and ensuring the stability of the online banking platform.

# I look forward to a swift resolution and a seamless banking experience moving forward.'''

#     print("Output of Model: ")
#     print(return_ans(content))
    
    
# if __name__ == "__main__":
#     test_output()
from json import loads

# Guard haystack imports and pipeline creation so this module can be imported
# even when django settings are not configured (e.g. in CI or simple local
# runs). If haystack/Django are not available/configured we fall back to a
# safe `return_ans` implementation that returns a default label.
HAYSTACK_AVAILABLE = False
try:
    from haystack import Document, Pipeline  # type: ignore
    from haystack_integrations.components.generators.ollama import OllamaGenerator  # type: ignore
    from haystack.components.preprocessors import DocumentCleaner  # type: ignore
    from haystack.components.builders.prompt_builder import PromptBuilder  # type: ignore
    from haystack.components.retrievers.in_memory import InMemoryBM25Retriever  # type: ignore
    from haystack.document_stores.in_memory import InMemoryDocumentStore  # type: ignore

    # Load the phishing dataset JSON (optional)
    with open('src/data/rag.json', 'r') as f:
        data = loads(f.read())

    docs = [Document(content=str(doc)) for doc in data['nodes']]

    cleaner = DocumentCleaner()
    ppdocs = cleaner.run(documents=docs)

    docu_store = InMemoryDocumentStore()
    docu_store.write_documents(ppdocs['documents'])

    retriever = InMemoryBM25Retriever(document_store=docu_store, top_k=3)

    template = '''
    You are a cybersecurity email inspection model.
    Your task is to determine whether the given email is PHISHING or NOT PHISHING.

    You MUST classify using strict cybersecurity rules.

    Context (security hint data):
    {% for document in documents %}
        {{ document.content }}
    {% endfor %}

    Email Text: {{ query }}

    Respond with EXACTLY ONE word:
    - "phishing" → if malicious intent, scam, password theft, impersonation, urgency trap, suspicious links, etc.
    - "not phishing" → if legitimate, harmless, normal communication
    '''

    prompt_builder = PromptBuilder(template=template)

    generator = OllamaGenerator(
        model="qwen:4b",
        url="http://localhost:11434",
        generation_kwargs={
            "num_predict": 10,
            "temperature": 0.1,
        },
    )

    rag_pipeline = Pipeline()
    rag_pipeline.add_component("retriever", retriever)
    rag_pipeline.add_component("prompt_builder", prompt_builder)
    rag_pipeline.add_component("llm", generator)
    rag_pipeline.connect("retriever", "prompt_builder.documents")
    rag_pipeline.connect("prompt_builder", "llm")

    HAYSTACK_AVAILABLE = True
except Exception as _e:
    # Avoid raising during import; other modules (UI, tests) can still run.
    print("Haystack pipeline not initialized (fallback):", _e)


def return_ans(query):
    # If haystack pipeline couldn't be initialized we return a safe default
    # so callers can continue to run without a configured Django/haystack.
    if not HAYSTACK_AVAILABLE:
        print("Haystack unavailable — returning default 'not phishing'")
        return "not phishing"

    try:
        print("Checking email...")
        ans = rag_pipeline.run({
            "prompt_builder": {"query": query[:5000]},
            "retriever": {"query": query[:5000]}
        })

        replies = ans.get("llm", {}).get("replies", [])
        if not replies:
            return "not phishing"

        label = replies[0].lower().strip()
        if "phish" in label:
            return "phishing"
        return "not phishing"

    except Exception as e:
        print("ERROR while running RAG pipeline:", e)
        return "not phishing"


def test_output():
    content = '''
    Dear customer, your bank account has been suspended due to unusual activity.
    Please update your credentials immediately using the link below:
    https://barclays.security-verify-login.com/update
    Failure to comply in 24 hours will result in access termination.
    '''

    print("RESULT:", return_ans(content))

# Collab

if __name__ == "__main__":
    test_output()
