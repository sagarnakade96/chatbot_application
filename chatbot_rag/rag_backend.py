import os 
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_aws import BedrockEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_classic.indexes import VectorstoreIndexCreator
from langchain_aws import ChatBedrockConverse
from botocore.config import Config

def hr_index() -> VectorstoreIndexCreator:
    try:
        # define the datasource for the documents
            data_loader = PyPDFLoader(
                "https://rikalp.in/wp-content/uploads/2024/07/HR-Policy.pdf"
            )
            print(f"data_loaded")

            

        
            # split the data for data cleaning and processing
            splitted_data = RecursiveCharacterTextSplitter(separators=["\n\n", "\n", " ", ""], chunk_size=1000, chunk_overlap=10)
            documents = data_loader.load()
            print(f"PDF loaded: {len(documents)} pages")

            chunks = splitted_data.split_documents(documents)
            print(f"Text split: {len(chunks)} chunks")

            
            # sample_data = "The Marvel Cinematic Universe (MCU) is an American media franchise and shared universe centered on a series of superhero films produced by Marvel Studios, based on characters from American comic books published by Marvel Comics. The franchise is owned by the Walt Disney Company and includes television series, short films, digital series, and literature. The shared universe, much like the original Marvel Universe in comic books, was established by crossing over common plot elements, settings, cast, and characters. Marvel Studios releases its films in groups called 'Phases', with the first three phases collectively known as 'The Infinity Saga' and the following three phases as 'The Multiverse Saga'. The first MCU film, Iron Man (2008), began Phase One, which culminated in the crossover film The Avengers (2012). Phase Two began with Iron Man 3 (2013) and concluded with Ant-Man (2015), while Phase Three began with Captain America: Civil War (2016) and concluded with Spider-Man: Far From Home (2019). Black Widow (2021) is the first film in Phase Four, which concluded with Black Panther: Wakanda Forever (2022), while Phase Five began with Ant-Man and the Wasp: Quantumania (2023) and concluded with Thunderbolts* (2025). Phase Six began with The Fantastic Four: First Steps (2025) and will conclude with Avengers: Secret Wars (2027)."
            # sample_data_2 = "The franchise has been commercially successful, becoming one of the highest-grossing media franchises of all time, and it has received generally positive reviews from critics. However, many of the Multiverse Saga projects performed below expectations and struggled compared to those of the Infinity Saga. The studio has attributed this to the increased amount of content produced after the 2019 film Avengers: Endgame, and began decreasing its content output as of 2024. The MCU has inspired other film and television studios to attempt similar shared universes and has also inspired several themed attractions, an art exhibit, television specials, literary material, multiple tie-in video games, and commercials."
            # final_data = sample_data + " " + sample_data_2 
            # try:
            #     data_split_test = splitted_data.split_text(final_data)
            #     print(data_split_test)
            # except Exception as e:
            #     print(f"Error occurred while splitting the data: {e}")
            aws_config = Config(
                connect_timeout=10,
                read_timeout=60,
                retries={
                    "max_attempts": 3,
                    "mode": "standard",
                },
            )
        
            data_embeddings = BedrockEmbeddings(credentials_profile_name="develop-admin",model_id="amazon.titan-embed-text-v1", region_name="us-east-1", config=aws_config)
            print(f"data embeddings {data_embeddings}")
            vector_store = FAISS.from_documents(chunks, data_embeddings)
            print("Embeddings and FAISS index created")
            # create a vector store for the data
            try:
                indexed_data = VectorstoreIndexCreator(
                            text_splitter=splitted_data,
                            embedding=data_embeddings,
                            vectorstore_cls=FAISS
                    
                        )
                print(f"vector_store_created")
            except Exception as e:
                print(f"Error occurred while creating the vector store: {str(e)}")
                return None
        
            # create an index for the data
            try:
                print("PDF loader configured")

                database_index = indexed_data.from_loaders([data_loader])

                print("PDF parsed, embedded, and FAISS index created")
                return database_index
            except Exception as e:
                print(f"Error occurred while creating the index: {str(e)}")
                return None
            
    except Exception as e:
        print(f"Error occurred while creating the index: {str(e)}")
        return None

def hr_llm():
    try:
        bedrock_llm = ChatBedrockConverse(
        credentials_profile_name="develop-admin",
        model = "us.anthropic.claude-sonnet-4-5-20250929-v1:0",
        region_name="us-east-1",
        temperature=0.1,
        max_tokens=1000,
    )
        return bedrock_llm
    except Exception as e:
        print(f"Error occurred while initializing BedrockLLM: {e}")
        return None


def rag_response(index, question):
    try:
        llm = hr_llm()
        if llm is None:
            return "Error: LLM initialization failed."
        response = index.query(question=question, llm=llm)
        return response
    except Exception as e:
        print(f"Error occurred while querying the index: {e}")
        return "Error: Querying the index failed."

