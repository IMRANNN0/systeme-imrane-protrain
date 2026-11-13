"""Render a deterministic color-reference chart from inspected public brand sources."""
import json
import re
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont

root=Path(__file__).resolve().parent
website='https://protraincompany.com/'
core=[
 {'key':'primary','name':'Primary green','hex':'#0A6B43','role':'Links, icons, green identity','css':'--o-color-1'},
 {'key':'secondary','name':'Amber','hex':'#F2A541','role':'Primary CTA and highlights','css':'--o-color-2'},
 {'key':'dark','name':'Forest dark','hex':'#0F2A1F','role':'Dark backgrounds, footer','css':'--o-color-5'},
 {'key':'light','name':'Ivory','hex':'#F6F4EE','role':'Light backgrounds','css':'--o-color-3'},
 {'key':'white','name':'White','hex':'#FFFFFF','role':'Surfaces and reversed text','css':'--o-color-4'},
 {'key':'body','name':'Body neutral','hex':'#212529','role':'Supporting body text','css':'--body-color'},
]
social=[
 {'key':'social_green','name':'Instagram green','hex':'#017A51','role':'Approximate encoded-image sample','source':'https://www.instagram.com/protrain_company/p/DX_uGqHiPWb/'},
 {'key':'social_yellow','name':'Instagram yellow','hex':'#F9CB2F','role':'Approximate encoded-image sample','source':'https://www.instagram.com/protrain_company/p/DX6hfjqiCOO/'},
]
proposed=[
 {'key':'comparison_blue','name':'Muted navy','hex':'#1E3A5F','role':'Optional second profile / comparison'},
 {'key':'soft_green','name':'Soft mint','hex':'#E7F3ED','role':'Optional quiet background / label'},
]
css=(root/'website-inline.css').read_text(encoding='utf-8')
for item in core:
 assert re.search(re.escape(item['css'])+r'\s*:\s*'+re.escape(item['hex']),css,re.I),item

def luminance(value):
 channels=[int(value[i:i+2],16)/255 for i in [1,3,5]]
 linear=[v/12.92 if v<=.04045 else ((v+.055)/1.055)**2.4 for v in channels]
 return sum(c*w for c,w in zip(linear,[.2126,.7152,.0722]))
def ratio(a,b):
 x,y=sorted([luminance(a),luminance(b)])
 return round((y+.05)/(x+.05),2)
pairs=[{'background':bg,'text':fg,'contrast_ratio':ratio(bg,fg)} for bg,fg in [
 ('#0A6B43','#FFFFFF'),('#F2A541','#0F2A1F'),('#017A51','#FFFFFF'),('#F9CB2F','#0F2A1F'),('#1E3A5F','#FFFFFF'),('#E7F3ED','#0F2A1F')]]
data={'reviewed_on':'2026-11-13','status':'Extracted working reference, not a supplied official brand manual',
 'website':{'source':website,'evidence':'website-inline.css + website.css + observed computed styles','confidence':'exact CSS values','colors':core},
 'instagram':{'source':'https://www.instagram.com/protrain_company/','confidence':'Visual samples and JPEG pixel estimates, not original design tokens','colors':social},
 'proposed_extensions':{'status':'Optional proposals, not extracted or approved','colors':proposed},
 'typography':{'latin':{'family':'Poppins','weights':[400,500,600,700]},'arabic':{'family':'Cairo','variable_weight_range':[200,1000]},
 'source':'Website @font-face declarations, unicode ranges and computed font stack','instagram_font':'Unconfirmed from raster examples','font_files_downloaded':False},
 'recommended_text_pairs':pairs,
 'style_observations':{'website':['Deep green hero with subtle texture/glow','Amber CTA with dark text','Pale backgrounds, white surfaces','Study/travel photography'],
 'instagram':['Study photography','Angled torn-edge green/white/yellow text strips','Green graduation-cap logo at top-left','Mint dotted texture and dashed flight route','Contact footer, green or white depending on sample']},
 'logo':{'file':'protrain-logo-site.png','source':'https://protraincompany.com/web/image/website/1/logo/0x128/ProTrain?unique=a9253c0','rule':'Use original artwork unchanged; this downloaded preview is not a vector master'},
 'scope':'Palette, typography and style only. Website copy changes do not revise approved product terms or ad claims.'}
(root/'protrain-palette.json').write_text(json.dumps(data,indent=2),encoding='utf-8')
lines=['/* ProTrain public-channel reference, 2026-11-13. IG samples approximate; extensions proposed. */',':root {']
for group in [core,social,proposed]:
 for item in group:lines.append(f"  --protrain-{item['key'].replace('_','-')}: {item['hex']};")
lines += ['  --protrain-font-latin: "Poppins", Arial, sans-serif;','  --protrain-font-arabic: "Cairo", Arial, sans-serif;','}',
 '.protrain-arabic { font-family: var(--protrain-font-arabic); letter-spacing: normal; direction: rtl; }',
 '.protrain-latin { font-family: var(--protrain-font-latin); }']
(root/'protrain-palette.css').write_text('\n'.join(lines)+'\n',encoding='utf-8')

# This is a measured color chart, not a replacement for generated photographic artwork.
image=Image.new('RGB',(1200,1260),'#FFFFFF');draw=ImageDraw.Draw(image)
font_path='C:/Windows/Fonts/arial.ttf';bold_path='C:/Windows/Fonts/arialbd.ttf'
def font(size,bold=False):return ImageFont.truetype(bold_path if bold else font_path,size)
draw.text((50,40),'PROTRAIN',font=font(49,True),fill='#0F2A1F')
draw.text((50,105),'Working color reference · 13 November 2026',font=font(24),fill='#4A5C54')
with Image.open(root/'protrain-logo-site.png').convert('RGBA') as logo:
 logo.thumbnail((105,100));image.paste(logo,(1040,35),logo)

def section(title,items,y):
 draw.text((50,y),title,font=font(26,True),fill='#0F2A1F')
 y+=45
 for i,item in enumerate(items):
  x=50+(i%2)*560;top=y+(i//2)*165
  draw.rectangle((x,top,x+535,top+98),fill=item['hex'],outline='#D8DFD9',width=1)
  foreground='#FFFFFF' if ratio(item['hex'],'#FFFFFF')>ratio(item['hex'],'#0F2A1F') else '#0F2A1F'
  draw.text((x+20,top+20),item['hex'],font=font(40,True),fill=foreground)
  draw.text((x,top+108),item['name'],font=font(25,True),fill='#212529')
 return y+((len(items)+1)//2)*165+8
y=section('01  WEBSITE · EXACT CSS TOKENS',core,175)
y=section('02  INSTAGRAM · APPROXIMATE IMAGE SAMPLES',social,y)
y=section('03  OPTIONAL EXTENSIONS · PROPOSED',proposed,y)
draw.text((50,y+8),'Website fonts: Poppins / Latin · Cairo / Arabic',font=font(25,True),fill='#0F2A1F')
draw.text((50,y+48),'Keep the original logo. Use dark text on amber/yellow.',font=font(22),fill='#4A5C54')
image.save(root/'protrain-palette-preview.png')
print(json.dumps({'core_tokens_verified':len(core),'social_samples':len(social),'proposed_colors':len(proposed),'text_pairs':pairs,'preview':'protrain-palette-preview.png'}))
