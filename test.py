import google.generativeai as genai
import os

genai.configure(api_key="AIzaSyC_PRyoRISOqWpgFJ1G_rUO9gM-2L_8EoM")

model = genai.GenerativeModel('gemini-pro')
response = model.generate_content('Please summarise this document: ...')

print(response.text)