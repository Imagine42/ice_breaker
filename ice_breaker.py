from dotenv import load_dotenv
import os
from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent
from third_parties.linkedin import scrape_linkedin_profile

if __name__ == "__main__":
    print("Hello LangChain!")
    load_dotenv()

    linkedin_profile_url = linkedin_lookup_agent(name="junseokpark")
    print(linkedin_profile_url)

    summary_template = """
    given the information {information} about a person I want you to create:
    1. A short summary
    2. two interesting facts about them
    """

    summary_prompt_template = PromptTemplate(
        input_variables=["information"], template=summary_template
    )

    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")

    chain = LLMChain(llm=llm, prompt=summary_prompt_template)

    linkedin_data = scrape_linkedin_profile(linkedin_profile_url=linkedin_profile_url)
    res = chain.invoke(input={"information": linkedin_data})

    print(res["text"])
