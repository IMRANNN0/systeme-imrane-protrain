import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { createRequire } from 'node:module';

const root = path.dirname(fileURLToPath(import.meta.url));
const require = createRequire(import.meta.url);
const sharp = require('C:/Users/Administrator/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/sharp');
const C = { green: '#0C4935', cream: '#F5F2E9', amber: '#E8AF43', muted: '#436557', line: '#B9C5B9' };
const logo = (await fs.readFile(path.join(root, 'assets/protrain-logo.png'))).toString('base64');
// librsvg on this host does not decode embedded WebP. Convert the unaltered
// source to PNG in memory for portable SVG image embedding.
const campus = (await sharp(path.join(root, 'assets/site-campus.webp')).png().toBuffer()).toString('base64');
const displayFont = (await fs.readFile('C:/Windows/Fonts/bahnschrift.ttf')).toString('base64');
const bodyFont = (await fs.readFile('C:/Windows/Fonts/arial.ttf')).toString('base64');
const esc = s => String(s).replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('>', '&gt;').replaceAll('"', '&quot;');
const rect = (x,y,w,h,fill) => `<rect x="${x}" y="${y}" width="${w}" height="${h}" fill="${fill}"/>`;
const line = (x1,y1,x2,y2,color=C.line,width=2) => `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${color}" stroke-width="${width}"/>`;
const tx = (s,x,y,size=38,fill=C.green,weight=400,font='Arial',extra='') => `<text x="${x}" y="${y}" font-family="${font}" font-size="${size}" font-weight="${weight}" fill="${fill}" ${extra}>${esc(s)}</text>`;
const display = (s,x,y,size=94,fill=C.green) => tx(s,x,y,size,fill,650,'Bahnschrift');
const label = (s,x,y,fill=C.muted) => tx(s,x,y,25,fill,600,'Arial','letter-spacing="2.1"');
const arrow = (x,y,color=C.green) => `<path d="M${x-27} ${y}H${x+23}M${x+6} ${y-17}l18 17-18 17" stroke="${color}" stroke-width="3.5" fill="none"/>`;
const header = (section,dark=false) => `${dark ? rect(72,40,128,119,C.cream):''}<image href="data:image/png;base64,${logo}" x="${dark?85:80}" y="${dark?50:47}" width="102" height="97"/>${label(section,242,105,dark?C.cream:C.muted)}${line(80,178,1000,178,dark?'#5D8271':C.line,1.5)}`;
const footer = (n,dark=false) => `${line(80,1266,1000,1266,dark?'#5D8271':C.line,1.5)}${tx('protraincompany.com',80,1313,25,dark?C.cream:C.green,400)}${tx(`${String(n).padStart(2,'0')} / 04`,1000,1313,25,dark?C.cream:C.green,600,'Arial','text-anchor="end"')}`;
function svg(title,description,body,bg=C.cream) {
 return `<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1350" viewBox="0 0 1080 1350" role="img" aria-label="${esc(title)}"><title>${esc(title)}</title><desc>${esc(description)}</desc><defs><style>@font-face{font-family:Bahnschrift;src:url(data:font/ttf;base64,${displayFont}) format('truetype')}@font-face{font-family:Arial;src:url(data:font/ttf;base64,${bodyFont}) format('truetype')}text{font-kerning:normal}</style></defs>${rect(0,0,1080,1350,bg)}${body}</svg>`;
}

const slides = [
 svg('Étudier à l’étranger, ça se prépare.', 'Présentation de l’agence ProTrain. Orientation, candidatures et visa étudiant. Photo de campus reprise du site officiel, sans attribution des personnes à ProTrain.',
  header('ÉTUDES À L’ÉTRANGER')+
  display('Étudier à',80,291,100)+display('l’étranger,',80,401,100)+display('ça se prépare.',80,511,100)+
  rect(82,549,90,8,C.amber)+
  tx('Orientation · Candidatures · Visa étudiant',80,610,36,C.green)+
  `<svg x="0" y="650" width="1080" height="600" viewBox="0 0 1600 1067" preserveAspectRatio="xMidYMid slice"><image href="data:image/png;base64,${campus}" width="1600" height="1067"/></svg>`+
  rect(80,1180,588,46,C.cream)+tx('Image de campus · source : site ProTrain',98,1211,25,C.green)+
  rect(0,1250,1080,100,C.green)+
  tx('protraincompany.com',80,1313,25,C.cream)+tx('01 / 04',1000,1313,25,C.cream,600,'Arial','text-anchor="end"')),
 svg('Un projet. Des étapes claires.', 'Les trois composantes de l’accompagnement : orientation, candidatures et dossier de visa étudiant. Les décisions appartiennent aux établissements et aux autorités compétentes.',
  header('L’ACCOMPAGNEMENT',true)+
  display('Un projet.',80,292,92,C.cream)+display('Des étapes claires.',80,391,84,C.cream)+
  line(80,473,1000,473,'#5D8271',1.5)+
  tx('01',80,541,42,C.amber,600,'Bahnschrift')+display('Orientation',174,541,48,C.cream)+
  tx('Comparer les programmes selon',174,596,38,C.cream)+tx('votre profil et votre projet.',174,646,38,C.cream)+
  line(80,688,1000,688,'#5D8271',1.5)+
  tx('02',80,756,42,C.amber,600,'Bahnschrift')+display('Candidatures',174,756,48,C.cream)+
  tx('Préparer les documents et',174,811,38,C.cream)+tx('comprendre les démarches.',174,861,38,C.cream)+
  line(80,903,1000,903,'#5D8271',1.5)+
  tx('03',80,971,42,C.amber,600,'Bahnschrift')+display('Visa étudiant',174,971,48,C.cream)+
  tx('Constituer votre dossier après',174,1026,38,C.cream)+tx('une admission.',174,1076,38,C.cream)+
  line(80,1117,1000,1117,'#5D8271',1.5)+
  tx('Admission : décision des établissements.',80,1170,32,C.cream)+
  tx('Visa : décision des autorités compétentes.',80,1217,32,C.cream)+footer(2,true),C.green),
 svg('À Guéliz. Et en ligne.', 'ProTrain reçoit les étudiants et les parents à Guéliz, Marrakech, ou en ligne. Adresse : Rue Ibn Aïcha. Aucune illustration ne représente un bureau réel.',
  header('RENCONTRONS-NOUS')+
  display('À Guéliz.',80,295,104)+display('Et en ligne.',80,407,104)+
  rect(83,446,91,8,C.amber)+
  tx('Étudiants et parents,',80,531,44,C.green)+tx('vous êtes les bienvenus.',80,588,44,C.green)+
  line(80,659,1000,659,C.line,1.5)+label('AU BUREAU',80,722)+
  display('Guéliz, Marrakech',80,792,60)+
  tx('Rue Ibn Aïcha',80,855,40,C.green)+
  `<path d="M921 720v124c0 28-30 28-30 54v38" fill="none" stroke="${C.green}" stroke-width="2"/><circle cx="921" cy="720" r="9" fill="${C.green}"/><circle cx="891" cy="936" r="8" fill="${C.amber}"/>`+
  rect(0,936,1080,314,C.green)+label('EN LIGNE',80,1002,C.amber)+
  display('Depuis chez vous.',80,1074,64,C.cream)+
  tx('Échangez avec notre équipe,',80,1141,40,C.cream)+tx('où que vous prépariez votre projet.',80,1193,40,C.cream)+
  footer(3)),
 svg('Parlons de votre projet.', 'Demander une consultation sur protraincompany.com/contactus. Demande, rappel d’un conseiller, organisation de la consultation. Conditions confirmées avant réservation.',
  header('VOTRE PREMIER ÉCHANGE')+
  display('Parlons de',80,291,100)+display('votre projet.',80,401,100)+
  rect(80,466,920,107,C.green)+display('Demander une consultation',110,535,43,C.cream)+arrow(942,520,C.cream)+
  tx('protraincompany.com/contactus',80,635,39,C.green,600)+
  label('LA SUITE DE VOTRE DEMANDE',80,733)+
  line(103,785,103,1061,C.line,2)+
  `<circle cx="103" cy="810" r="23" fill="${C.green}"/>`+tx('1',103,821,29,C.cream,600,'Arial','text-anchor="middle"')+
  tx('Vous présentez votre projet.',158,823,39,C.green)+
  `<circle cx="103" cy="925" r="23" fill="${C.green}"/>`+tx('2',103,936,29,C.cream,600,'Arial','text-anchor="middle"')+
  tx('Un conseiller vous recontacte.',158,938,39,C.green)+
  `<circle cx="103" cy="1040" r="23" fill="${C.green}"/>`+tx('3',103,1051,29,C.cream,600,'Arial','text-anchor="middle"')+
  tx('Vous organisez la consultation.',158,1053,39,C.green)+
  line(80,1110,1000,1110,C.line,1.5)+
  tx('Conditions confirmées',80,1171,36,C.green)+tx('avant la réservation.',80,1219,36,C.green)+footer(4))
];

const validation = [];
for (let i=0;i<slides.length;i++) {
 const name=`slide-${String(i+1).padStart(2,'0')}`;
 await fs.writeFile(path.join(root,`${name}.svg`),slides[i],'utf8');
 const result=await sharp(Buffer.from(slides[i])).png({compressionLevel:9}).toFile(path.join(root,`${name}.png`));
 validation.push({file:`${name}.png`,width:result.width,height:result.height,format:result.format,bytes:result.size});
 if(result.width!==1080 || result.height!==1350) throw new Error(`${name}: wrong dimensions`);
}
const gutter=28;
const items=[];
for(let i=0;i<4;i++) {
 const input=await sharp(path.join(root,`slide-${String(i+1).padStart(2,'0')}.png`)).resize(540,675).toBuffer();
 items.push({input,left:gutter+(i%2)*(540+gutter),top:gutter+Math.floor(i/2)*(675+gutter)});
}
await sharp({create:{width:1164,height:1434,channels:3,background:'#D9DDD6'}}).composite(items).png().toFile(path.join(root,'contact-sheet.png'));
await fs.writeFile(path.join(root,'validation.json'),JSON.stringify({canvas:{width:1080,height:1350},slides:validation,contactSheet:{width:1164,height:1434},fonts:['Bahnschrift','Arial'],imagesEmbedded:true,externalPublication:false},null,2),'utf8');
await fs.writeFile(path.join(root,'caption.txt'),`باغي تكمل قرايتك فالخارج؟ فـProTrain كنرافقو الطلبة والوالدين فـorientation، candidatures وdossier de visa étudiant.\n\nتقدر تلاقى الفريق فـGuéliz بمراكش، أو تتواصل معانا en ligne.\n\nتعرّف على الخدمات فـprotraincompany.com، وإذا بغيتي تهضر على المشروع ديالك، قدّم demande de consultation من صفحة Contact:\nhttps://protraincompany.com/contactus\n\nالشروط كتتأكد قبل réservation.\n`,'utf8');
await fs.writeFile(path.join(root,'preview.html'),`<!doctype html><html lang="fr"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>ProTrain — Présentation de l’agence</title><style>body{margin:0;background:#e0e3dc;color:#0C4935;font:18px Arial,sans-serif}main{max-width:1164px;margin:32px auto;padding:0 20px}h1{font-size:26px}p{line-height:1.5}.slides{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:24px}img{display:block;width:100%;height:auto}figure{margin:0}figcaption{padding:12px 0 20px}@media(max-width:650px){.slides{grid-template-columns:1fr}}</style><main><h1>ProTrain — Présentation de l’agence</h1><p>4 visuels de production · 1080 × 1350 px · Proposition non publiée</p><div class="slides">${slides.map((s,i)=>`<figure><img src="slide-0${i+1}.png" alt="${['Étudier à l’étranger, ça se prépare.','Un projet. Des étapes claires.','À Guéliz. Et en ligne.','Parlons de votre projet.'][i]}"><figcaption>0${i+1} / 04 — <a href="slide-0${i+1}.svg">Source SVG éditable</a></figcaption></figure>`).join('')}</div><p><a href="caption.txt">Caption Darija</a> · <a href="contact-sheet.png">Vue d’ensemble</a></p></main></html>`,'utf8');
console.log(JSON.stringify(validation,null,2));
