from crewai_tools import DirectoryReadTool, FileReadTool, SerperDevTool, BaseTool
import os
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool
from langchain_openai import ChatOpenAI
import streamlit as st

os.environ["SERPER_API_KEY"] = "2203d27aa32a1d92275134fb632bf009714b2476" # serper.dev API key
os.environ["OPENAI_API_BASE"] = 'https://api.agicto.cn/v1'
os.environ["OPENAI_MODEL_NAME"] ='gpt-4o-mini'  # Adjust based on available model
os.environ["OPENAI_API_KEY"] = 'sk-bmzsXFgX4CgCUCoC22IgfGhRomJLvd2M8EI74JuNWij3YRPJ'

llm = ChatOpenAI(model="gpt-4o-mini")

# Define the agents
class SalesAgents:
    def __init__(self):
        self.llm = llm

    def sales_rep_agent(self):
        return Agent(
            role="Sales Representative",
            goal="Identify high-value leads that match our ideal customer profile",
            backstory=(
                "As a key member of the dynamic sales team at COMET Estimating LLC, your mission is to navigate the construction and "
                "estimating sectors to uncover promising leads. Leveraging state-of-the-art tools and a strategic approach, "
                "you delve into data, market trends, and industry interactions to identify opportunities that others might miss. "
                "Your role is essential in fostering valuable connections and driving the growth of our estimating services, "
                "ensuring that general contractors and subcontractors benefit from precise, actionable insights and expert support."
            ),
            allow_delegation=False,
            verbose=True,
            llm=self.llm,
            # max_iter=15,
            memory=True,
            max_iter=2
        )

    def lead_sales_rep_agent(self):
        return Agent(
            role="Lead Sales Representative",
            goal="Nurture leads with personalized, compelling communications",
            backstory=(
                "Within the dynamic landscape of crewAI's sales department, you excel as the crucial link "
                "between prospective clients and the estimating solutions they require. By crafting tailored, engaging communications, "
                "you not only showcase our expert services but also ensure that general contractors and subcontractors feel understood and valued. "
                "Your role is key in transforming interest into tangible outcomes, guiding leads from initial curiosity through to securing our "
                "estimating services."
            ),
            allow_delegation=False,
            verbose=True,
            llm=self.llm,
            # max_iter=15,
            memory=True,
            max_iter=2
        )
# Define the tools
directory_read_tool = DirectoryReadTool(directory='./content')
file_read_tool = FileReadTool()
search_tool = SerperDevTool()

class SentimentAnalysisTool(BaseTool):
    name: str = "Sentiment Analysis Tool"
    description: str = ("Analyzes the sentiment of text to ensure positive and engaging communication according to context.")

    def _run(self, text: str) -> str:
        # Custom sentiment analysis logic
        return "positive"

sentiment_analysis_tool = SentimentAnalysisTool()

# Define the tasks
class SalesTasks:
    def lead_profiling_task(self):
        return Task(
            description=(
                """
                Conduct a thorough analysis of [Lead Name], a general contractor or subcontractor in the construction sector that
                recently expressed interest in our estimating services. Utilize all available data sources, including industry databases,
                company websites, LinkedIn, and recent news articles, to compile a comprehensive profile. This profile should include:

                1. Identification of key decision-makers within the company, such as project managers or procurement officers.
                2. A summary of recent project developments or contracts that the company is involved in.
                3. An assessment of their specific needs related to estimating services, such as budgeting, cost forecasting, or bidding accuracy.

                Ensure that all the information used is accurate and verified, as this analysis will be crucial for customizing our
                engagement strategy to effectively meet the company’s needs.
                """
            ),
            expected_output=(
                "A detailed report on {lead_name}, covering company background, key personnel, recent projects, and specific needs related to estimating services. "
                "Identify potential areas where our estimating solutions can add value and propose customized engagement strategies."
            ),
            tools=[directory_read_tool, file_read_tool, search_tool],
            agent=SalesAgents().sales_rep_agent()
        )

    def personalized_outreach_task(self):
        return Task(
            description=(
                """
                Work at an estimating company where you are tasked with targeting general contractors or subcontractors in the construction sector.
                Using insights from sales representative agents and the lead profiling report on {lead_name}, create a personalized outreach campaign for targeting {key_decision_maker},
                the {position} of {lead_name}. The campaign should address their recent project developments and demonstrate how our estimating services can enhance their operations.
                Your communication must align with {lead_name}'s company culture and demonstrate a clear understanding of their needs and objectives.
                Ensure all information is accurate and verified.

                In the dynamic world of sales, you act as the crucial link between potential clients and the services they need.
                By crafting tailored, engaging communications, you not only showcase the strengths of the services offered but also ensure that clients feel understood and valued,
                particularly when targeting general contractors or subcontractors in the construction sector.
                Your role is key in transforming interest into actionable outcomes, guiding leads from initial curiosity to securing the service offered.
                Adapt these strategies to effectively connect with any company looking to engage with similar clients.
                """
            ),
            expected_output=(
                "A series of customized email drafts for {lead_name}, specifically directed at {key_decision_maker}. "
                "Each draft should clearly connect our estimating services with their recent project developments and goals. "
                "The tone should be professional, engaging, and consistent with {lead_name}'s company culture."
            ),
            tools=[sentiment_analysis_tool, search_tool],
            agent=SalesAgents().lead_sales_rep_agent()
        )
# Create the crew
crew = Crew(
    agents=[
        SalesAgents().sales_rep_agent(),
        SalesAgents().lead_sales_rep_agent()
    ],
    tasks=[
        SalesTasks().lead_profiling_task(),
        SalesTasks().personalized_outreach_task()
    ],
    verbose=True,
    memory=True
)
inputs = {
    "lead_name": "COMET ESTIMATING LLC",
    "industry": "Contrution Estimaing COMPANY in USA",
    "key_decision_maker": "Mustafa Shoukat",
    "position": "President/CEO",
    "milestone": "product launch"

}

# Run the crew tasks
result = crew.kickoff(inputs=inputs)

# Print the result
st.write(result)