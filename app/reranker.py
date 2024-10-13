import os
from langchain_openai import ChatOpenAI


from dotenv import load_dotenv
load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv('OPENAI_API_KEY')
# Initialize the language model
llm = ChatOpenAI(model="gpt-4o-mini", temperature = 0)



def re_rank_jobs(user_profile, job_list):
    re_ranked_jobs = []

    for index, job in job_list.iterrows():
        prompt = f"""
    You are an expert career advisor.

    *Important Notes (Please read carefully):**
    1. A **degree** and a **diploma** are not equivalent.
    2. If a job requires a **degree**, having a **diploma**, even in a relevant field, does **not** meet this requirement.
    3. If the user does not meet the minimum educational requirements, the **Rating must be 1**, regardless of other factors.
    4. Assign a rating based strictly on the user's alignment with the job requirements.
    5. Use only the information provided; do not make assumptions.
    6. Provide the output strictly in the requested format.
    
    Given the following user profile and a job description, rate the suitability of the job for the user on a scale from 1 to 10 (10 being a perfect match).
    Give bonus points if the user has a related degree or diploma to what is required in the job.
    Also create a roadmap to suggest tasks or certificates the user should take on to be better suited for the role.
    
    **User Profile:**
    Interests: {user_profile['interest']}
    Education: {user_profile['certification']}
    Job History: {user_profile['job history']}
    Experience: {user_profile['years of experience']}
    Skills : {user_profile['skills']}
    
    **Job Profile**
    Title: {job['Job Title']}
    Description: {job['Job Description']}
    Requirements: {job['Requirements']}
    
    Provide your rating and a brief justification in the following format:
    
    Rating: [1-10]
    Justification: [Your explanation]
    Roadmap: [Your suggested roadmap]
    """

        # Create the message for the LLM
        messages = [{"role": "user", "content": prompt}]

        # Call the LLM using LangChain's ChatOpenAI
        response = llm(messages)

        # Extract the assistant's message
        assistant_message = response.content.strip()

        # Parse the rating and justification
        rating, justification, roadmap = parse_response(assistant_message)

        # Append the result to the re_ranked_jobs list
        re_ranked_jobs.append({
            'job': job,
            'rating': rating,
            'justification': justification,
            'roadmap': roadmap,
        })

    # Sort the jobs based on the rating in descending order
    re_ranked_jobs.sort(key=lambda x: x['rating'], reverse=True)

    return re_ranked_jobs


def parse_response(response_text):
    import re

    # Use regular expressions to extract the rating, justification, and roadmap
    rating_match = re.search(r'Rating:\s*(\d+)', response_text)
    justification_match = re.search(r'Justification:\s*(.*?)\s*Roadmap:', response_text, re.DOTALL)
    roadmap_match = re.search(r'Roadmap:\s*(.*)', response_text, re.DOTALL)

    if rating_match:
        rating = int(rating_match.group(1))
    else:
        rating = 0  # Default rating if not found

    if justification_match:
        justification = justification_match.group(1).strip()
    else:
        justification = "No justification provided."

    if roadmap_match:
        roadmap = roadmap_match.group(1).strip()
    else:
        roadmap = "No roadmap provided."

    return rating, justification, roadmap

#############SAMPLE DATA
import pandas as pd

job_file = "job_descriptions.csv"
job_df = pd.read_csv(job_file, encoding='utf-8')


user_file = "MOCK_DATA (6).csv"

user_df = pd.read_csv(user_file, encoding='utf-8')
user = user_df.iloc[328] # Bachelor of Engineering with Honours in Electrical Power Engineering [Degree]
###############
re_ranked_jobs = re_rank_jobs(user, job_df)
filtered_jobs = [job for job in re_ranked_jobs if job['rating'] >= 5]
if not filtered_jobs:
    print("No recommendations available.")

else:
    top_k = 3
    top_three_jobs = filtered_jobs[:top_k]

    # Display the up to top three jobs
    print("Job Recommendations:")
    for idx, job_info in enumerate(top_three_jobs, start=1):
        job = job_info['job']
        print("-" * 60)
        print(f"Rank {idx}: {job.get('Job Title', 'Not specified')}")
        print(f"Rating: {job_info['rating']}/10")
        print(f"Justification:\n{job_info['justification']}")
        print(f"Roadmap:\n{job_info.get('roadmap', 'No roadmap provided.')}")
    print("-" * 60)


