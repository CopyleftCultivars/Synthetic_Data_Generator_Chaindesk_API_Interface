import csv
import requests
import logging
import random
import pandas as pd

# Replace with your Chaindesk API token
API_TOKEN = "YOUR CHAINDESK API TOKEN HERE"

# Replace with your Chaindesk agent ID
AGENT_ID = "YOUR CHAINDESK AGENT ID HERE"

# Path to the CSV file for storing prompts and responses
DATA_FILE = "prompts_and_responses.csv"

# List of location entities
LOCATIONS = [
    "France", "Italy", "Spain", "Germany", "Tibet", "Washington State", "Ghana", "India", "China", "Brazil", "Australia", "Canada", "Mexico", "Argentina", "Chile", "South Africa", "New Zealand", "Japan", "South Korea", "Thailand", "Vietnam", "Indonesia", "Philippines", "Malaysia", "Singapore", "Taiwan", "Hong Kong", "Macau", "Laos", "Cambodia", "Myanmar", "Bangladesh", "Pakistan", "Afghanistan", "Iran", "Iraq", "Saudi Arabia", "United Arab Emirates", "Qatar", "Oman", "Oregon", "California", "Idaho", "Montana", "Wyoming", "Colorado", "Utah", "Nevada", "Arizona", "New Mexico", "Texas", "Oklahoma", "Kansas", "Nebraska", "South Dakota", "North Dakota", "Minnesota", "Iowa", "Missouri", "Arkansas", "Louisiana", "Mississippi", "Alabama", "Georgia", "Florida", "South Carolina", "North Carolina", "Virginia", "West Virginia", "Kentucky", "Tennessee", "Ohio", "Michigan", "Wisconsin", "Illinois", "Indiana", "Pennsylvania", "New York", "Vermont", "New Hampshire", "Maine", "Massachusetts", "Rhode Island", "Connecticut", "New Jersey", "Delaware", "Maryland", "Washington, D.C.", "Hawaii", "Alaska", "Puerto Rico", "U.S. Virgin Islands", "Guam", "American Samoa", "Northern Mariana Islands", "Bermuda", "Bahamas", "Cuba", "Jamaica", "Haiti", "Dominican Republic", "Puerto Rico", "Virgin Islands", "Guatemala", "Belize", "Honduras", "El Salvador", "Nicaragua", "Costa Rica", "Panama", "Colombia", "Venezuela", "Ecuador", "Peru", "Bolivia", "Paraguay", "Uruguay", "Guyana", "Suriname", "French Guiana", "Portugal", "Spain", "France", "Monaco", "Andorra", "Italy", "San Marino", "Turkey", "Acre Brasil", "Acre Brazil", "Peruvian highlands", "Peruvian lowlands", "Malta", "Greece", "Cyprus", "Turkey", "Bulgaria", "Romania", "Moldova", "Ukraine", "Belarus", "Lithuania", "Latvia", "Estonia", "Finland", "Sweden", "Norway", "Denmark", "Iceland", "United Kingdom", "Ireland", "Netherlands", "Belgium", "Luxembourg", "Germany", "Switzerland", "Liechtenstein", "Austria", "Czech Republic", "Slovakia", "Hungary", "Slovenia", "Croatia", "Bosnia and Herzegovina", "Serbia"
    # Add more locations as needed
]

# List of crop entities
CROPS = [
    "chicken", "rice", "corn", "vegetables", "wheat", "various crops", "fruit trees", "grapes", "olives", "silvopasture trees with cattle", "figs", "blueberries", "blackberries", "apples", "pears", "peaches", "cherries", "plums", "apricots", "nectarines", "almonds", "walnuts", "pistachios", "hazelnuts", "pecans", "macadamia nuts", "cashews", "pumpkins", "squash", "zucchini", "cucumbers", "tomatoes", "peppers", "eggplant", "lettuce", "spinach", "kale", "collard greens", "chard", "arugula", "broccoli", "cauliflower", "cabbage", "brussels sprouts", "carrots", "beets", "radishes", "turnips", "rutabagas", "parsnips", "potatoes", "sweet potatoes", "yams", "onions", "garlic", "shallots", "leeks", "scallions", "chives", "celery", "fennel", "asparagus", "artichokes", "okra", "green beans", "snap peas", "snow peas", "edamame", "lentils", "chickpeas", "black beans", "pinto beans", "kidney beans", "navy beans", "lima beans", "cannellini beans", "garbanzo beans", "soybeans", "mung beans", "adzuki beans", "black-eyed peas", "split peas", "peanuts", "sunflowers", "flax", "hemp", "cannabis", "marijuana", "quinoa", "amaranth", "buckwheat", "millet", "sorghum", "rye", "barley", "oats", "spelt", "teff", "wild rice", "couscous", "bulgur", "farro", "kamut", "emmer", "einkorn", "wheat berries", "strawberries",
    # Add more crops as needed
]

# List of entities to fill in the prompt templates
ENTITIES = [
    "photosynthesis", "scientific methodology in farming", "soil food web", "regenerating soil fertility after synthetic fertilizer abuse", "cellular respiration", "fermentation", "IMO-3", "IMO", "lactic acid bacteria", "yeast", "fungal diseases", "enzymes", "septoria", "powdery mildew", "botrytis", "spider mites", "IPM (Integrated Pest Management)", "Cho Natural Farming", "JADAM Natural Farming", "fertilizer production", "history of indigenous farming", "soil health", "composting", "vermicomposting", "biodynamic farming", "permaculture", "agroforestry", "silvopasture", "polyculture", "cover cropping", "crop rotation", "no-till farming", "conservation tillage", "strip-till farming", "ridge-till farming", "mulching", "green manure", "crop residues", "biochar", "rock dust", "compost tea", "manure tea", "fish emulsion", "seaweed extract", "bone meal", "FPJ", "FFJ", "FAA", "Fish Amino Acids", "alfalfa growth hormones", "the harms of pesticides", "organic farming", "biodynamic farming", "regenerative agriculture", "sustainable agriculture", "agroecology", "food sovereignty", "food security", "food justice", "food deserts",
    # Add more entities as needed
]

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def generate_data(num_prompts):
    """
    Generates synthetic data by querying the Chaindesk agent with prompts and saving responses to a CSV file.

    Args:
        num_prompts: The number of prompts to generate and query the agent with.
    """
    prompts = generate_prompts(num_prompts)

    with open(DATA_FILE, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Prompt", "Response"])

        for prompt in prompts:
            try:
                response = query_agent(prompt)
                writer.writerow([prompt, response])
                logging.info(f"Prompt: {prompt}\nResponse: {response}\n")
                print(f"Prompt: {prompt}\nResponse: {response}\n")
            except requests.exceptions.RequestException as e:
                logging.error(f"Error querying agent: {e}")

PROMPT_TEMPLATES = [
    "Located in {location} with a {farm_size} acre farm growing {crop1} and {crop2}. How can I switch to regenerative and natural farming methods?",
    "What are the best practices for farming {crop1}, {crop2}, and {crop3} on a {farm_size} acre farm in {location}?",
    "How do I create fertilizers for {crop1} and {crop2} in {location}?",
    "I am in {location} with a {farm_size} acre farm growing {crop1}. How can I improve soil health and fertility?",
    "What are the benefits of renegerative or natural farming for {crop1} farming in {location}?",
    "{location} with {crop1} and {crop2}. Tell me about {entity}.",
    "{location}, {crop1}, {entity}",
    "How can I use {entity} to improve soil health and fertility in {location}?",
    "Explain {entity} to me",
    "I'd like to know about {entity}.",
    # Add more prompt templates as needed
]

def generate_prompts(num_prompts):
    """
    Generates a list of prompts by randomly filling in prompt templates with entities.

    Args:
        num_prompts: The number of prompts to generate.

    Returns:
        A list of prompts.
    """
    prompts = []
    for _ in range(num_prompts):
        template = random.choice(PROMPT_TEMPLATES)
        location = random.choice(LOCATIONS)
        farm_size = str(random.randint(0, 80))
        crop1 = random.choice(CROPS)
        crop2 = random.choice(CROPS)
        crop3 = random.choice(CROPS)
        crop = random.choice(CROPS)
        entity = random.choice(ENTITIES)
        prompt = template.format(location=location, farm_size=farm_size, crop1=crop1, crop2=crop2, crop3=crop3, crop=crop, entity=entity)
        prompts.append(prompt)
    return prompts

def query_agent(prompt):
    """
    Queries the Chaindesk agent with a prompt and returns the response.

    Args:
        prompt: The prompt to query the agent with.

    Returns:
        The response from the Chaindesk agent.
    """
    url = f"https://api.chaindesk.ai/agents/{AGENT_ID}/query"
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json",
    }
    data = {
        "query": prompt,
        "streaming": False,
    }

    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()["answer"]

num_prompts_count = 100
while num_prompts_count > 0:
    generate_data(3)
    num_prompts_count -= 3
    # Calculate the number of prompts created
    num_prompts_created = 1000 - num_prompts_count
    # Print the number of prompts created
    print(f"Successfully created {num_prompts_created} prompts.")

# Untested section: save column 1 as prompts and column 2 as responses in DATA_FILE csv
# Read the CSV file
data = pd.read_csv(DATA_FILE)

# Save column 1 as prompts and column 2 as responses
data.rename(columns={"Prompt": "prompts", "Response": "responses"}, inplace=True)

# Save the updated data to the CSV file
data.to_csv(DATA_FILE, index=False)

logging.info(f"Data for {num_prompts_created} prompts saved to {DATA_FILE}")