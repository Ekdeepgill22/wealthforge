#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from niveshwala.crew import NiveshWala


warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")
warnings.filterwarnings("ignore", category=DeprecationWarning, module="pydantic")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """
    inputs = {
    'symbol': input("Enter the stock symbol (e.g., AAPL, TSLA, RELIANCE.NS): "),
    'topic': input("Enter the main research topic (e.g., 'Q2 earnings analysis', 'risk evaluation', 'market trends'): "),
    'sector': input("Enter the sector/industry (e.g., Technology, Finance, Energy): "),
    'region': str("India"),
    'investment_horizon': input("Enter the investment horizon (e.g., short-term, mid-term, long-term): "),
    'risk_profile': input("Enter the risk profile (e.g., low, medium, high): "),
    'current_year': str(datetime.now().year)
}

    try:
        result = NiveshWala().crew().kickoff(inputs=inputs)
        print('--------------result---------------')
        print(result.raw)
        print('--------------result---------------')
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


# def train():
#     """
#     Train the crew for a given number of iterations.
#     """
#     inputs = {
#         "topic": "AI LLMs",
#         'current_year': str(datetime.now().year)
#     }
#     try:
#         NiveshWala().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

#     except Exception as e:
#         raise Exception(f"An error occurred while training the crew: {e}")

# def replay():
#     """
#     Replay the crew execution from a specific task.
#     """
#     try:
#         NiveshWala().crew().replay(task_id=sys.argv[1])

#     except Exception as e:
#         raise Exception(f"An error occurred while replaying the crew: {e}")

# def test():
#     """
#     Test the crew execution and returns the results.
#     """
#     inputs = {
#         "topic": "AI LLMs",
#         "current_year": str(datetime.now().year)
#     }
    
#     try:
#         NiveshWala().crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)

#     except Exception as e:
#         raise Exception(f"An error occurred while testing the crew: {e}")
