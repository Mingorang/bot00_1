"""Build Agent using Microsoft Agent Framework in Python
# Run this python script
> pip install agent-framework==1.0.0rc6
> python <this-script-path>.py
"""

import asyncio
import os
from dotenv import load_dotenv

from agent_framework_foundry import FoundryAgent
from azure.identity.aio import DefaultAzureCredential

load_dotenv()

# User inputs for the conversation
USER_INPUTS = [
    "can you see or access this csv below, and if so output a standard candle style chart of the result, with a 28% confidence interval of results and a fast and slow average line (blue and yellow)\n\nDate,Open,High,Low,Close\n2026-09-14 09:00:00,100.0,109.3722,98.7909,109.3678\n2026-09-14 10:00:00,109.3678,123.8213,107.6063,123.819\n2026-09-14 11:00:00,123.819,123.8193,109.435,110.4499\n2026-09-14 12:00:00,110.4499,117.0916,110.1829,117.0876\n2026-09-14 13:00:00,117.0876,117.0917,101.8224,102.0028\n2026-09-14 14:00:00,102.0028,122.6698,99.9629,122.6677\n2026-09-14 15:00:00,122.6677,122.6707,106.9226,106.9441\n2026-09-14 16:00:00,106.9441,106.9481,80.9042,82.2614\n2026-09-14 17:00:00,82.2614,83.1254,81.5511,83.1252\n2026-09-15 09:00:00,83.1252,83.1284,77.5384,78.5575\n2026-09-15 10:00:00,78.5575,95.8376,77.2681,95.8339\n2026-09-15 11:00:00,95.8339,115.1519,94.6529,115.1467\n2026-09-15 12:00:00,115.1467,119.1103,113.31,119.1052\n2026-09-15 13:00:00,119.1052,138.364,117.6693,138.3638\n2026-09-15 14:00:00,138.3638,143.7952,138.056,143.7948\n2026-09-15 15:00:00,143.7948,144.2952,143.3211,144.2918\n2026-09-15 16:00:00,144.2918,165.6737,143.3314,165.6684\n2026-09-15 17:00:00,165.6684,179.9648,162.3384,179.9564\n2026-09-16 09:00:00,179.9564,179.964,176.0019,177.6987\n2026-09-16 10:00:00,177.6987,177.7046,158.6686,160.6604\n2026-09-16 11:00:00,160.6604,168.9307,160.3858,168.9284\n2026-09-16 12:00:00,168.9284,175.6471,165.0719,175.6406\n2026-09-16 13:00:00,175.6406,178.8139,174.9149,178.8117\n2026-09-16 14:00:00,178.8117,178.8177,163.1409,163.7819\n2026-09-16 15:00:00,163.7819,163.7832,147.977,148.9871\n2026-09-16 16:00:00,148.9871,174.5072,146.8333,174.5042\n2026-09-16 17:00:00,174.5042,174.5045,148.0809,149.6481\n2026-09-17 09:00:00,149.6481,158.465,149.3905,158.4585\n2026-09-17 10:00:00,158.4585,158.4599,142.1159,144.4137\n2026-09-17 11:00:00,144.4137,144.4156,136.5784,138.8292\n2026-09-17 12:00:00,138.8292,167.0311,135.8998,167.0256\n2026-09-17 13:00:00,167.0256,176.6467,164.6975,176.6432\n2026-09-17 14:00:00,176.6432,176.6482,159.0377,162.7909\n2026-09-17 15:00:00,162.7909,185.599,159.976,185.5913\n2026-09-17 16:00:00,185.5913,200.5423,182.0976,200.5354\n2026-09-17 17:00:00,200.5354,200.5385,173.5868,177.181\n2026-09-18 09:00:00,177.181,177.1849,166.359,166.8347\n2026-09-18 10:00:00,166.8347,195.3395,163.6025,195.3312\n2026-09-18 11:00:00,195.3312,209.222,194.1213,209.2187\n2026-09-18 12:00:00,209.2187,209.2251,199.0152,199.2697\n2026-09-18 13:00:00,199.2697,206.0756,197.4708,206.0694\n2026-09-18 14:00:00,206.0694,212.4574,203.3108,212.4492\n2026-09-18 15:00:00,212.4492,212.4581,187.0289,188.3909\n2026-09-18 16:00:00,188.3909,188.3966,174.7288,178.1315\n2026-09-18 17:00:00,178.1315,189.0623,177.2824,189.0556",
]

async def main() -> None:
    # For authentication, DefaultAzureCredential supports multiple authentication methods. Run `az login` in terminal for Azure CLI auth.
    async with FoundryAgent(
        project_endpoint=os.environ["AZURE_AI_PROJECT_ENDPOINT"],
        agent_name="bot00",
        agent_version="3",
        credential=DefaultAzureCredential(),
    ) as agent:
    
        # Process user messages
        for user_input in USER_INPUTS:
            print(f"\n# User: '{user_input}'")
            printed_tool_calls = set()
            async for chunk in agent.run(user_input, stream=True):
                # log tool calls if any
                function_calls = [
                    c for c in chunk.contents
                    if c.type == "function_call"
                ]
                for call in function_calls:
                    if call.call_id not in printed_tool_calls:
                        print(f"Tool calls: {call.name}")
                        printed_tool_calls.add(call.call_id)
                if chunk.text:
                    print(chunk.text, end="", flush=True)
            print("")

        print("\n--- All tasks completed successfully ---")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nProgram interrupted by user")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("Program finished.")
