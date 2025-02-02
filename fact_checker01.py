from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.chains import SimpleSequentialChain
import sys

#send open ai api key
OPENAI_API_KEY="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"

def fact_check(question):
    llm = OpenAI(temperature=0.7, openai_api_key=OPENAI_API_KEY) # pass openai_api_key here
    template = """{question}\n\n"""
    prompt_template = PromptTemplate(input_variables=["question"], template=template)
    question_chain = LLMChain(llm=llm, prompt=prompt_template)

    template = """Here is a statement:
    {statement}
    Make a bullet point list of the assumptions you made when producing the above statement.\n\n"""
    prompt_template = PromptTemplate(input_variables=["statement"], template=template)
    assumptions_chain = LLMChain(llm=llm, prompt=prompt_template)

    template = """Here is a bullet point list of assertions:
    {assertions}
    For each assertion, determine whether it is true or false using google search as a second and third source. If it is false, explain why.\n\n"""
    prompt_template = PromptTemplate(input_variables=["assertions"], template=template)
    fact_checker_chain = LLMChain(llm=llm, prompt=prompt_template)

    template = """In light of the above facts, how would you answer the question '{}'""".format(question)
    template = """{facts}\n""" + template
    prompt_template = PromptTemplate(input_variables=["facts"], template=template)
    answer_chain = LLMChain(llm=llm, prompt=prompt_template)

    overall_chain = SimpleSequentialChain(chains=[question_chain, assumptions_chain, fact_checker_chain, answer_chain], verbose=True)

    return overall_chain.run(question)

if __name__=="__main__":
    if len(sys.argv) > 1:
        question = sys.argv[1]
    else:
        question = "how can La Paz be the world's highest official capital when it isn't the official capital of Bolivia?"
    print(question)
    answer = fact_check(question)
    print(answer)
