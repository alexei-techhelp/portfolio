import re
import os
import urllib.request
import urllib.parse
import json
import time

md_file = r"d:\Antigravity\Про мене\Portfolio_Projects\FULL_PORTFOLIO_FOR_NOTION.md"
data_js_file = r"d:\Antigravity\Про мене\Portfolio_Web\data.js"

with open(md_file, "r", encoding="utf-8") as f:
    text = f.read()

sections = text.split('\n# ')
projects_js = "const projects = [\n"

def parse_md_to_html(text):
    # Parse images first before formatting other things
    text = re.sub(r'!\[([^\]]*)\]\((.*?)\)', r'<img src="\2" alt="\1" class="w-full rounded-xl border border-gray-800 my-6 shadow-2xl object-cover">', text)
    
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong class="text-white">\1</strong>', text)
    text = re.sub(r'- (.*)', r'<li>\1</li>', text)
    text = re.sub(r'(<li>.*?</li>\n?)+', lambda m: f'<ul class="list-disc pl-5 my-2 space-y-1">{m.group(0)}</ul>', text)
    text = text.replace('\n', '<br>')
    return text

def translate_ua_to_en(text):
    if not text.strip(): return ""
    url = "https://translate.googleapis.com/translate_a/single?client=gtx&sl=uk&tl=en&dt=t&q=" + urllib.parse.quote(text)
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        response = urllib.request.urlopen(req)
        data = json.loads(response.read().decode('utf-8'))
        translated = "".join([sentence[0] for sentence in data[0] if sentence[0]])
        # Fix markdown spacing
        translated = translated.replace('** ', '**').replace(' **', '**')
        return translated
    except Exception as e:
        print("Error translating:", e)
        return text

proj_idx = 0
for i, section in enumerate(sections):
    if not section.strip() or "Portfolio" in section.split('\n')[0]:
        continue
    
    lines = section.strip().split('\n')
    title = lines[0].strip().replace("'", "\\'")
    title_en = translate_ua_to_en(title).replace("'", "\\'")
    
    body = '\n'.join(lines[1:])
    subsections = body.split('\n## ')
    
    content_ua = ""
    content_en = ""
    summary_ua = ""
    summary_en = ""
    
    tags_list = []
    text_lower = section.lower()
    tech_map = {
        'n8n': 'n8n',
        'make.com': 'Make.com',
        'baserow': 'Baserow',
        'gemini': 'Gemini',
        'vertex': 'Vertex AI',
        'python': 'Python',
        'fastapi': 'FastAPI',
        'docker': 'Docker',
        'manychat': 'Manychat',
        'linkedin': 'LinkedIn',
        'telegram': 'Telegram',
        'facebook': 'Facebook',
        'cloudinary': 'Cloudinary',
        'google sheets': 'Google Sheets',
        'grpc': 'gRPC',
        'firecrawl': 'Firecrawl',
        'userbot': 'Userbot',
        'pdf': 'PDF RAG',
        'openai': 'OpenAI'
    }
    for kw, tag in tech_map.items():
        if kw in text_lower and tag not in tags_list:
            tags_list.append(tag)
    
    if not tags_list:
        tags_list = ['AI', 'Automation']
        
    tags_str = str(tags_list[:5])

    for sub in subsections:
        if not sub.strip(): continue
        sub_lines = sub.strip().split('\n')
        h3 = sub_lines[0].replace('## ', '').strip()
        p = '\n'.join(sub_lines[1:])
        
        h3_en = translate_ua_to_en(h3)
        p_en = translate_ua_to_en(p)
        
        p_html_ua = parse_md_to_html(p)
        p_html_en = parse_md_to_html(p_en)
        
        if "Проблема" in h3 and not summary_ua:
            clean_p_ua = re.sub(r'<[^>]+>', '', p).replace('\n', ' ')
            summary_ua = clean_p_ua[:180].strip() + "..."
            clean_p_en = re.sub(r'<[^>]+>', '', p_en).replace('\n', ' ')
            summary_en = clean_p_en[:180].strip() + "..."
            
        content_ua += f'<h3 class="text-xl font-bold mt-8 mb-3 text-accent">{h3}</h3>\n<div class="text-gray-300 leading-relaxed text-sm md:text-base">{p_html_ua}</div>\n'
        content_en += f'<h3 class="text-xl font-bold mt-8 mb-3 text-accent">{h3_en}</h3>\n<div class="text-gray-300 leading-relaxed text-sm md:text-base">{p_html_en}</div>\n'
        
        time.sleep(0.3)

    content_ua = content_ua.replace('`', '\\`').replace('\\r', '')
    content_en = content_en.replace('`', '\\`').replace('\\r', '')
    summary_ua = summary_ua.replace('`', '\\`').replace('\\r', '').replace('\\n', ' ')
    if not summary_en: summary_en = summary_ua
    summary_en = summary_en.replace('`', '\\`').replace('\\r', '').replace('\\n', ' ')

    images_array = [
        "assets/ai_content.png",
        "assets/content_v2.png",
        "assets/ecommerce_banner.png",
        "assets/event_crm.png",
        "assets/influencer.png",
        "assets/reels.png",
        "assets/pdf_rag.png",
        "assets/n8n_arch.png",
        "assets/telegram.png",
        "assets/travel.png",
        "assets/voice_banner.png"
    ]
    
    image_url = images_array[proj_idx] if proj_idx < len(images_array) else "https://images.unsplash.com/photo-1677442136019-21780ecad995?auto=format&fit=crop&q=80&w=800"

    js_obj = f"""
    {{
        id: "proj_{proj_idx}",
        image: "{image_url}",
        title: {{
            en: `{title_en}`,
            ua: `{title}`
        }},
        tags: {tags_str},
        summary: {{
            en: `{summary_en}`,
            ua: `{summary_ua}`
        }},
        content: {{
            en: `{content_en}`,
            ua: `{content_ua}`
        }}
    }},"""
    projects_js += js_obj
    proj_idx += 1

projects_js += "\n];\n"

with open(data_js_file, "r", encoding="utf-8") as f:
    old_data = f.read()

translations_part = old_data.split('const projects')[0].strip()

with open(data_js_file, "w", encoding="utf-8") as f:
    f.write(translations_part + "\n\n" + projects_js)

print("Build successful.")
