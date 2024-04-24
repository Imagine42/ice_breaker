import os
from dotenv import load_dotenv

load_dotenv()
from langchain.chat_models import ChatOpenAI
from langchain.prompts.prompt import PromptTemplate
from langchain_core.tools import Tool
from langchain.agents import (
    create_react_agent,
    AgentExecutor,
)
from langchain import hub

from tools.tools import get_profile_url


def lookup(name: str) -> str:
    """
    Lookup a LinkedIn profile by name and return the profile information.
    """
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
    template = """
    given the full name {name_of_person} of a person I want you to get it me a link to their Linkedin profile page.
    your answer should contain only a URL
    """
    prompt_template = PromptTemplate(
        template=template, input_variables=["name_of_person"]
    )

    tools_for_agent = [
        Tool(
            name="Crawl Google 4 linkedin profile page",
            func=get_profile_url,
            description="useful for when you need get the Linkedin page URL",
        )
    ]

    react_prompt = hub.pull("hwchase17/react")
    agent = create_react_agent(
        llm=llm,
        tools=tools_for_agent,
        prompt=react_prompt,
    )
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools_for_agent,
        verbose=True,
    )

    result = agent_executor.invoke(
        input={"input": prompt_template.format_prompt(name_of_person=name)}
    )

    linked_profile_url = result["output"]

    # agent = initialize_agent(
    #     llm=llm,
    #     tools=tools_for_agent,
    #     agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    #     verbose=True,
    # )

    # linked_profile_url = agent.run(prompt_template.format_prompt(name_of_person=name))

    return linked_profile_url


if __name__ == "__main__":
    print("Hello LangChain!")

    linkedin_profile_url = lookup(name="junseokpark")
    print(linkedin_profile_url)
    print("Done!")
