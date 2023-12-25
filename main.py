from pathlib import Path
from dotenv import load_dotenv
load_dotenv(dotenv_path=(Path(__file__).parent / ".env").absolute())

import re
from langchain.llms import OpenAI
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
from langchain.callbacks import StdOutCallbackHandler


USER_DESCRIPTION = """This tool retrieves the user's name. This tool can only be used if the id_numbers can be obtained from the user's question. Otherwise, its usage is prohibited.
Input to the tool should be a json string with 2 keys: "id_number" and "output_instructions".
The value of this "id_number" must be an 18-digit number. If the value cannot be obtained from the question, leave it blank instead of fabricating a value.
The value of "output_instructions" should be instructions on what information to extract from the response.
"""

CRIMINAL_DESCRIPTION = """This tool retrieves detailed information about criminal charges. This tool can only be used when the charge can be obtainedfrom the user's question. Otherwise, its usage is prohibited.
Input to the tool should be a json string with 2 keys: "criminal" and "output_instructions".
The value of this "criminal" must be a category of charges. If the value cannot be obtained from the question, leave it blank instead of fabricating a value.
The value of "output_instructions" should be instructions on what information to extract from the response.
"""

SUMMARY_TEMPLATE = """This is user's question: {user_input}
This is the answer: {answer}
Please summarize and answer in Chinese.
"""

llm = OpenAI(temperature=0, streaming=True, max_tokens=1000)

def user_func(input):
    pattern = r'"id_number":\s*"(\d+)"'
    match = re.search(pattern, input)

    if match:
        id_number = match.group(1)
        return f"姓名：李旺，身份证号：{id_number}"
    return ''
    
def criminal_func(input):
    pattern = r'"criminal":\s*"([^"]+)"'
    match = re.search(pattern, input)

    if match:
        criminal = match.group(1)
        return f"{criminal}罪，判处有期徒刑十年"
    return ''


tools = [
    Tool(
        name="user",
        description=USER_DESCRIPTION,
        func=user_func,
    ),
    Tool(
        name="criminal",
        description=CRIMINAL_DESCRIPTION,
        func=criminal_func,
    ),
]

mrkl = initialize_agent(
    tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True, max_iterations=10
)

callback = StdOutCallbackHandler()

q1 = "查询下这个人的姓名，123456789123456789"
print(q1)
answer = mrkl.run(q1, callbacks=[callback])
print(f'任务答案：{answer}')
print(f'最终答案： {llm.predict(SUMMARY_TEMPLATE.format(user_input=q1, answer=answer))}\n\n')


q2 = "盗窃罪怎么判"
print(q2)
answer = mrkl.run(q2, callbacks=[callback])
print(f'任务答案：{answer}')
print(f'最终答案： {llm.predict(SUMMARY_TEMPLATE.format(user_input=q2, answer=answer))}')
