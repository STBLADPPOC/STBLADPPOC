import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
print("Base Directory => ",BASE_DIR)

CONTENT_STORE_URL = '/ContentStore/'
CONTENT_STORE_DIRS = [
    os.path.join(BASE_DIR, CONTENT_STORE_URL),
]

print("this is static dir: ",CONTENT_STORE_DIRS)

STB_HOME = 'https://www.stb.gov.sg/content/stb/en.html'
VISIT_SG = 'https://www.visitsingapore.com/en/'
ORCHID_HOME = ''


