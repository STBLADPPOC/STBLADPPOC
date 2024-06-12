import requests
from bs4 import BeautifulSoup
# Function to convert worksheet to list of lists
def read_excel_to_list(pd, file_path, sheet_name=0):
    try:
        # Read the Excel file into a DataFrame
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        # Convert DataFrame rows to a list of lists
        lines = df.values.tolist()
        return lines
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        return []
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return []
    
 # Function to slice values from lists of lists
def get_values(url_list):
    values = []
    for sublist in url_list:
        values.extend(sublist)
    return values[1::2]

#check if text entered is ascii
def isEnglish(s):
  return s.isascii()

print(isEnglish(" 读写汉字 - 学中文"))
  #return s.translate(None, s.punctuation).isalnum()

def extract_url_stb_home():
 url = 'https://www.stb.gov.sg/'
 reqs = requests.get(url)
 soup = BeautifulSoup(reqs.text, 'html.parser')
 urls = []
 for link in soup.find_all('a'):
  if 'stan' in str(link):
   continue
  if 'tih' in str(link):
   continue
  if 'trust' in str(link):
   continue
  if 'visitor-information' in str(link):
   continue
  if '/content/' in str(link):
   urls.append("https://www.stb.gov.sg"+str(link.get('href')))
 print(urls)
 print(len(urls))
 return urls

extract_url_stb_home()