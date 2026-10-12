from package_file import HumanMessage
from llm_file import llm
from tools import attach_name
def generate_a_story(state):
    """This function takes the current state of the story agent and invokes the LLM to generate a response based on the topic and story provided in the state.
    """
    topic = state.get("topic", "")
    story = state.get("story", "")
    context = "Generate a story based on the given topic and story. The story shall be 4-5 sentences long. Provide an improvised version of the story and a final version of the story. Also welcome the user with a personalized message using the attach_name tool."
    messages = [
        HumanMessage(
            content=f"{context}\nTopic: {topic}\nStory: {story}\nImprovised Story: {state.get('improvised_story', '')}\nFinal Story: {state.get('final_story', '')}"
        )
    ]
    response_with_tool = llm.bind_tools(tools=[attach_name])
    response = response_with_tool.invoke(messages)
    return {
        "story": [response]
    }

def resolve_conflicted_story(state):
    """This function takes the current state of the story agent and invokes the LLM to resolve any conflicts in the story based on the topic and story provided in the state.
    """
    story = state.get("story", "")
    if "?" in story or "!" in story:
        return "Fail"
    return "Pass"


def improved_story(state):
    """This function takes the current state of the story agent and invokes the LLM to generate an improved version of the story based on the topic and story provided in the state.
    """
    topic = state.get("topic", "")
    story = state.get("story", "")
    context = "Generate an improved version of the story based on the given topic and story. The improved story shall be 4-5 sentences long."
    improved_messages = [
        HumanMessage(
            content=f"{context}\nTopic: {topic}\nStory: {story}\nImprovised Story: {state.get('improvised_story', '')}\nFinal Story: {state.get('final_story', '')}"
        )
    ]
    response = llm.invoke(improved_messages)
    return {
        "story": [response]
    }

def polished_story(state):
    """This function takes the current state of the story agent and invokes the LLM to generate a polished version of the story based on the topic and story provided in the state.
    """
    topic = state.get("topic", "")
    story = state.get("story", "")
    context = "Add an unexpected twist to the story based on the given topic and story. The polished story shall be 4-5 sentences long."
    polished_messages = [
        HumanMessage(
            content=f"{context}\nTopic: {topic}\nStory: {story}\nImprovised Story: {state.get('improvised_story', '')}\nFinal Story: {state.get('final_story', '')}"
        )
    ]
    response = llm.invoke(polished_messages)
    return {
        "final_story": [response]
    }