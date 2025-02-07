import requests
from bs4 import BeautifulSoup

# URL of the page to scrape
url = "https://brainlox.com/courses/category/technical"

# Fetch the HTML content
response = requests.get(url)
print("HTML content fetched successfully.")  # Debugging message

# Check if the request was successful
if response.status_code == 200:
    html_content = response.text

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Extract relevant course data (adjust the class name if needed)
    courses = soup.find_all('h2', class_='entry-title')  # Adjust the class name if needed

    # Print out the course titles
    if courses:
        for course in courses:
            print(course.text.strip())  # Print course names
    else:
        print("No courses found. Please check the HTML structure.")
else:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
print(soup.prettify()[:1000])  # Print the first 1000 characters of the HTML
