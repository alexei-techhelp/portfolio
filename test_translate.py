import urllib.request
import urllib.parse
import json

def translate_ua_to_en(text):
    if not text.strip(): return ""
    url = "https://translate.googleapis.com/translate_a/single?client=gtx&sl=uk&tl=en&dt=t&q=" + urllib.parse.quote(text)
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        response = urllib.request.urlopen(req)
        data = json.loads(response.read().decode('utf-8'))
        translated = "".join([sentence[0] for sentence in data[0] if sentence[0]])
        return translated
    except Exception as e:
        print("Error translating:", e)
        return text

test_text = """**Керування даними (Baserow):** Як архітектурне рішення я обрав Baserow замість Airtable, щоб обійти жорсткі ліміти."""
print("Original:", test_text)
print("Translated:", translate_ua_to_en(test_text))
