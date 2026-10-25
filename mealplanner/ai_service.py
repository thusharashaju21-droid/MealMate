
import os
from dotenv import load_dotenv
load_dotenv()
from google import genai

api_key = os.getenv("api_key")

client = genai.Client(api_key=api_key)

def get_diet_plan(response_data):

    monthly_total_calorie = response_data.get("monthly_total_calorie")
    category_total_calorie = response_data.get("category_total_calorie")

    category_total_calorie_text = ""

    for di in category_total_calorie:

        category_total_calorie_text += f". {di.get("meal_type")} : {di.get("total")}\n"

    prompt = f"""
                Act as an expert food diet advisor specializing in daily diet and calorie intaking in Kerala, India.

                Here is my monthly diet plan summary for last month:
                - Total Monthly calorie: ₹{monthly_total_calorie:,}
                - meal_type Breakdown:{category_total_calorie_text}
            

                Based on this data, please provide a practical 1-month Kerala diet plan:
                1. *diet Analysis: Point out high-calorie and protein areas relative to typical Kerala living costs.
                2. Optimized 1-Month diet Plan: Suggest a revised diet plan breakdown using standard allocation rules (e.g., amount of calorie and protein intake daily.
                3. Actionable Kerala-Specific diet Tips:* Provide 3-4 realistic ways to reduce calorie locally .
                """

    response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt
        )

    return response.text