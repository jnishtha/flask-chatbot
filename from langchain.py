import requests
from bs4 import BeautifulSoup
import nltk
nltk.download('averaged_perceptron_tagger')


from langchain_community.document_loaders import UnstructuredURLLoader


# List of URLs to scrape
urls = ["https://brainlox.com/courses/category/technical"]

# fetch the html content
response = requests.get(urls)
html_content = response.text

# Load data from the URL
loader = UnstructuredURLLoader(urls=urls)
docs = loader.load()
# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Extract relevant course data (modify as per the actual structure)
courses = soup.find_all('h2', class_='entry-title')  # Adjust the class name if needed

# Print out the course titles
for course in courses:
    print(course.text.strip())

# # Print extracted text
# for doc in docs:
#     print(doc.page_content[:1000])  # Display only first 1000 characters

#save extracted data
with open("courses.txt","w",encoding="utf-8") as f:
    for doc in docs:
        f.write(doc.page_content + "\n\n")

# Print success message
print("✅ Data saved to courses.txt")

# Read the extracted data from courses.txt
with open('courses.txt', 'r', encoding='utf-8') as file:
    courses_data = file.readlines()

# Print the first 3 lines for verification
print(courses_data[:3])