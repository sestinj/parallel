import openai
from dotenv import load_dotenv
import os

load_dotenv()
openai.api_key = os.environ.get("OPENAI_API_KEY")

def singular(q: str):
    return openai.Completion.create(
            engine="davinci",
            prompt=f"Q: {q}\nA:",
            temperature=0.5,
            max_tokens=50,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0.6,
            stop=["\n"],
        ).choices[0].text

def parallel(q: str, items: list[str]):
    responses = []
    for item in items:
        prompt = f"Answer concisely:\nQ: {q.replace('{}', item)}\nA:"
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            temperature=0.5,
            max_tokens=50,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0.6,
            stop=["\n"],
        )
        responses.append(response.choices[0].text)
    return responses

def parallel_one_question(q: str, items: list[str]):
    prompt = f"""For each of the items in the list, answer the following question, replacing the "{{}}" with the item:
-------------------
Items: New York, Michigan, Alabama, California, Texas
Question: What is the capitol of {{}}?
Answers:
New York: New York City
Michigan: Lansing
Alabama: Montgomery
California: Sacremento
Texas: Austin
-------------------
Items: {", ".join(items)}
Question: {q}
Answers:"""
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        temperature=0.5,
        max_tokens=150,
        top_p=1,
    )
    return response.choices[0].text

def generate_list(category: str):
    prompt = f"Q: Give a full, comma-separated list of {category}.\nA:"
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        temperature=0.5,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6,
    )
    return response.choices[0].text

# Should be able to ask a question to generate the list of items
# Like "Who are all of the players to play for the LA Lakers?"
# Should be able to specify a format for the answer?
# Need to figure out a prompt to get a consice answer.
# Might want to make flashcards with the answers.

if __name__ == "__main__":
    print("Welcome to Parallel! You can ask any question, and if you ask with {} as a placeholder, you can ask the question for each of several values to take its place.")
    print("""Example:
    Ask a question: How many {} are there in the world?
    Enter values: people, cats, dogs, turtles, cows, fish
    Response: ...Try it to see!""")
    while True:
        inp = input("Ask a question: ")
        if "{}" in inp:
            values_okay = False
            while not values_okay:
                values = input("Enter values (or Enter to generate them): ").split(", ")
                if values == ['']:
                    prompt = input("Generate a list of: ")
                    values = generate_list(prompt).split(", ")
                    print(f"Generated {len(values)} values: ", ", ".join(values))
                    values_okay = input(f"Are these values okay? (y/n): ") == "y"
                else:
                    values_okay = True

            responses = parallel_one_question(inp, values)
            print("Answers:")
            print(responses)
            # for value, response in zip(values, responses):
            #     print(f"{value}: {response}")
        else:
            print("Answer:", singular(inp))
        print("-----------------------------------------------")