# Web Scraper for Content and Images

This Python script scrapes a webpage for content and images inside a div with the class toc-content. The script automatically creates a unique folder for each URL, naming it based on the h1 tag of the page. The images found in the toc-content div are downloaded into this folder.

## Features

Automatic Folder Creation: A new folder is created for each URL based on the h1 tag of the page and the current timestamp. Scrapes Content and Images: The script downloads all images within the specified div (toc-content), and saves them with filenames based on the page's h1. Clean Code: The script uses best practices for clean, maintainable code.

## Requirements

Python 3.x pip for managing Python packages requests and beautifulsoup4 libraries

## How to Install Python and pip

Install Python

Windows:

Download the latest version of Python from python.org.
During installation, make sure to check the box that says "Add Python to PATH."
Open a terminal or command prompt and verify Python is installed by running:
```
python --version
```
macOS/Linux: Python 3 is typically pre-installed on macOS and Linux. To check if Python is installed, open a terminal and run:
```
python3 --version
```
If Python is not installed, install it using brew (for macOS) or your package manager for Linux:

macOS (via Homebrew) brew install python

Install pip

pip is included with Python installations. To check if pip is installed, run:
```
pip --version
```
If pip is not installed, run the following command:
```
python -m ensurepip --upgrade
```
Verify that pip was installed correctly by running:
```
pip --version
```
## Installation and Setup

Clone the repository

To get started with this project, clone the repository using the following command:
```
git clone https://github.com/MartinPotoniec/lin-image-scraper.git cd lin-image-scraper
```
Install the required dependencies

Once inside the project folder, install the necessary libraries using pip:
```
pip install -r requirements.txt
```
This command installs the requests and beautifulsoup4 libraries needed for the script.

## How to Use the Script

Running the Script

To run the script, simply enter the following command into your terminal:
```
python3 script.py https://example.com/1
```
What Happens When You Run the Script?

Folder Creation: The script will automatically create a folder in the images/ directory. The folder will be named based on the h1 tag of the page you scraped, appended with a timestamp to ensure uniqueness. Image Download: All images found inside the div class=toc-content will be saved in the newly created folder. The images will be named based on the page’s h1 tag, followed by the image number.

## Example Walkthrough

Suppose you run the following command:
```
python3 script.py https://example.com/1
```
If the page has an h1 with the text "Headline ", the script will create a folder named like images/Headline_20241022-153045/. Inside this folder, the script will download all images found in the div class=toc-content and name them like Headline_image_1.jpg, Headline_image_2.jpg, etc.

### Folder Structure

After running the script, your folder structure will look something like this:
```
images/ Headline_20241022-153045/ Headline_image_1.jpg Headline_image_2.jpg
```
### Error Handling

If no div class=toc-content is found, the script will notify you that no content was found to scrape. If the webpage does not contain an h1 tag, the script will use no_h1 as the folder name.

#### Additional Notes

The script ensures that each URL results in a new folder, so images from different webpages are never overwritten. The folder names are based on the h1 tag and a timestamp to ensure unique folder names even for the same webpage.