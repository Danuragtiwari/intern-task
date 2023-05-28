import requests
from bs4 import BeautifulSoup
import pytesseract
# import urllib.parse
from PIL import Image
# from io import BytesIO
# import pdfminer
# from pdfminer.high_level import extract_text
# from pdfminer.high_level import extract_text_to_fp

# Captcha Solver
def captcha_solver():
    captcha_image = Image.open('captcha.png')
    captcha_text = pytesseract.image_to_string(captcha_image)
    # print(captcha_text)
    return captcha_text



def download_voter_list(district):
    # Step 1: Create a session object
    session = requests.Session()

    # Step 2: Visit the website and retrieve initial data
    url = 'https://ceoelection.maharashtra.gov.in/searchlist/'
    response = session.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # For District
    district_select = soup.find('select', id='ctl00_Content_DistrictList')
    district_option = district_select.find('option', string=district)
    district_value = district_option['value']
    form = soup.find("form", id="aspnetForm")
    viewstate = form.find("input", id="__VIEWSTATE")["value"]
    viewstategenerator = form.find("input", id="__VIEWSTATEGENERATOR")["value"]
    eventvalidation = form.find("input", id="__EVENTVALIDATION")["value"]
    captcha_url = form.find("img", alt="")["src"]  # URL of the captcha image

    # Form data for initial request
    ac_value = '48'
    revision_value = '1'
    language_value = '1'
    part_value = '1'
    form_data = {
        "__VIEWSTATE": viewstate,
        "__VIEWSTATEGENERATOR": viewstategenerator,
        "__EVENTVALIDATION": eventvalidation,
        'ctl00$Content$DistrictList': district_value,
        'ctl00$Content$AssemblyList': ac_value,
        'ctl00$Content$listrollrevision': revision_value,
        'ctl00$Content$LangTypepdf': language_value,
        'ctl00$Content$PartList': part_value,
        'ctl00$Content$txtcaptcha': '',
        'ctl00$Content$OpenButton': 'Open PDF'
    }

    # Step 3: Submit the initial form data
    # 

    
    # Extract the captcha image URL
    captcha_image_url = 'https://ceoelection.maharashtra.gov.in/searchlist/Captcha.aspx'

    # Download the captcha image
    captcha_image_response = session.get(captcha_image_url, stream=True)
    with open('captcha.png', 'wb') as captcha_image_file:
        captcha_image_file.write(captcha_image_response.content)

    # Manually type the captcha
        
    captcha_text = captcha_solver()
    print(captcha_text)

    # Update the form data with the extracted captcha text
    form_data['ctl00$Content$txtcaptcha'] = captcha_text
    # print(form_data)
    response = requests.post(url, data=form_data)
    print(response)
    

    # # Download the PDF
    with open('output.pdf', 'wb') as file:
        file.write(response.content)
   

district = 'Nagpur'
download_voter_list(district)
