"""Build an offline analysis report, never a creative or reconstructed template."""
from pathlib import Path
import hashlib
import html
import json

ROOT = Path(__file__).resolve().parent
COMPONENT = ROOT.parent.parent
inventory = json.loads((ROOT / 'inventory-measurements.json').read_text(encoding='utf-8'))
geometry = json.loads((ROOT / 'reference-32-geometry.json').read_text(encoding='utf-8'))
selected = Path(geometry['file'])

groups = [
    {'name': 'A — Photo plein cadre et dégradé vert', 'ids': [18, 21, 26, 28, 33, 35, 37], 'grammar': 'Photo dominante en haut; vert progressif en bas; bandes blanches et texte jaune directement sur le vert. #21 utilise deux niveaux; #28 ajoute des carrés de ponctuation. Footer blanc.'},
    {'name': 'B — Photo et quatre rubans décalés', 'ids': [22, 24, 31], 'grammar': 'Photo plein cadre, dégradé vert, alternance de rubans blancs et jaunes avec retraits variables. #31 ajoute une phrase sous les rubans. Footer blanc.'},
    {'name': 'C — Papier clair et trois rubans contigus', 'ids': [19, 23, 27, 29, 30, 32, 34], 'grammar': 'Fond papier froissé clair; sujet central; points menthe et trajet pointillé; rubans vert/jaune/blanc; footer vert. Les bulles de #29, drapeaux de #32 et ponctuations de #30/#34 sont des variantes propres à ces références.'},
    {'name': 'D — Déclinaison verticale Story', 'ids': [25], 'grammar': '480 × 854, deux rubans vert/jaune, sujet debout. Ce n’est pas le même gabarit que le Feed 4:5.'},
    {'name': 'E — Publications événementielles', 'ids': [17, 20], 'grammar': 'Aïd et fête du Travail: calligraphie, étoiles ou calendrier spécifiques. Ne pas les importer dans le gabarit Match.'},
]

proposal = {
    'status': 'PROPOSED_REFERENCE_AWAITING_IMRAN_APPROVAL',
    'date': '2026-11-13',
    'authorized_scope': 'Analysis and proposal only. Stop before reconstruction or Creative01V4.',
    'reference': {'path': selected.as_posix(), 'sha256': hashlib.sha256(selected.read_bytes()).hexdigest(), 'size': [864,1080], 'id':32},
    'selection_reason': 'Existing orientation-confusion subject, surrounding choices and three substantial text ribbons. Yellow and white ribbons already support two lines. One actual composition; no merging with #29 bubbles or photo-family gradients.',
    'output_if_approved': {'size':[1080,1350], 'uniform_scale':1.25, 'phone_review':[360,450]},
    'locked': [
        'Canvas ratio and uniform scaling; no stretch or automatic crop',
        'Original corporate logo artwork, natural aspect ratio and measured upper-left anchor',
        'Paper texture, pale halftone dots, dashed route, z-order and soft shadows from #32 only',
        'Three torn ribbons: green/yellow/white order, geometry, rotation, overlapping and internal margins',
        'Typography hierarchy, weights and sizes once identified and approved; no automatic font shrinking',
        'Main-image mask/anchor and five badge geometries, positions, count and shadows',
        'Footer silhouette, icons and current reference contact content unless Imran explicitly approves an exception',
    ],
    'variable_slots': {
        'hook': {'text':'كتوجد لـCampus France ومحتار فاختيار الـFormations؟', 'proposed_region':'green ribbon'},
        'promise': {'text':'عمّر ملفك الدراسي، واكتشف جوج تكوينات مقترحة مع معلومات تساعدك تفهم اختياراتك.', 'proposed_region':'yellow ribbon, existing two-line region'},
        'cta': {'text':'شوف جوج Formations مجاناً', 'proposed_region':'white ribbon, existing text treatment; no new button'},
        'main_image': {'scope':'One student visual within the measured subject region; foreground overlap remains unchanged. No generated or extracted asset prepared in this phase.'},
        'choice_badge_contents': {'status':'REQUIRES_APPROVAL', 'scope':'Replace country-flag imagery with illustrative academic-choice content; retain five original circles and their geometry. No badge labels/icons selected or created yet. Not actual recommendations.'},
    },
    'unresolved': [
        'Exact Instagram font families, font sizes and numeric weights cannot be recovered reliably from flattened raster; source file or designer font metadata needed.',
        'Website Cairo/Poppins are verified existing brand candidates, not certified Instagram fonts; Arabic companion and weight require approval.',
        'Current long mixed-script hook may not fit original one-line green ribbon at locked type scale. No layout or font-size change is authorized silently.',
        'Five country flags communicate multiple destinations; leaving them unchanged would conflict with France-only program matching. Badge content adaptation is proposed only.',
        'Reference footer www.protrain.ma and phone are historical visible contact details; their current suitability for the Match funnel was not verified here. No changes made.',
        'The reference has no Match product label. Corporate logo stays unchanged; any new editable Match identifier and its placement need an explicit approved exception to the locked reference.',
        'Original high-resolution/vector logo, isolated student photo, clean paper/halftone/route layers and exact torn-edge paths were not located. Faithful reconstruction would be approximate without them.',
    ],
    'proposed_future_layers': [
        '00_reference — immutable original and hash, hidden from export',
        '10_background — locked paper, halftone and route',
        '20_subject — replaceable bitmap in locked mask and anchor',
        '30_choices — five locked badge frames; approved variable interiors only',
        '40_logo — original corporate asset unchanged; no invented logo',
        '50_ribbons — locked paper shapes, colors, rotation, shadow and z-order',
        '60_copy — editable hook/promise/CTA with explicit RTL and isolated French runs',
        '70_footer — locked original geometry and contact artwork',
    ],
    'future_preflight': [
        'Get reference/slot/exception approval before reconstructing or generating V4.',
        'Render original reference wording first, compare side by side and with an opacity overlay; report geometry/color/type deviations. No misleading similarity score.',
        'Only then insert exact approved Match copy and designated variable assets.',
        'Validate mixed-script visual reading order and manual line breaks at 1080×1350 and 360×450, not source strings alone.',
        'Reject overflow, clipping or unreadable copy. Stop for a specific decision instead of changing words, shrinking text or altering locked geometry.',
        'Inspect logo fidelity, selected-reference colors, badge semantics, offer accuracy and all introduced elements.',
        'Hash originals again. Preserve previous versions. Deliver editable source and PNG for Imran review; no Creative02 or launch.',
    ],
    'claims': {'basis':'Latest owner copy and saved landing-page read-only inspection from 2026-11-13', 'free_entry':'Two programs after profile entry; paid complete report remains separate', 'limits':'No form/matching/report/payment exercised. Original reference admission/accompaniment wording is not a Match claim. No price in the ad.'},
    'production_performed': False,
}
(ROOT / 'template-proposal.json').write_text(json.dumps(proposal, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')

# Root's independent pixel/position review supplements the worker's measurements.
review = {
    'date':'2026-11-13', 'status':'ANALYSIS_COMPLETE_NOT_CREATIVE_APPROVAL',
    'independent_review':'Controller viewed supplied collection, then decoded #32 and #29 originals at full size; reviewed worker evidence and independently sampled #32 pixels.',
    'sample_method':'Pillow RGB, per-channel median and exact RGB mode, no source edits',
    'independent_samples': [
        {'roi':[70,665,150,705], 'role':'green ribbon', 'mode':'#017950', 'median':[5,121,82]},
        {'roi':[75,792,130,825], 'role':'yellow ribbon', 'mode':'#F9CB30', 'median':[249,203,48]},
        {'roi':[55,907,90,965], 'role':'white ribbon', 'mode':'#FFFFFF', 'median':[255,255,255]},
        {'roi':[180,160,210,200], 'role':'clear paper', 'mode':'#EFEFEF', 'median':[234,234,234]},
        {'roi':[0,1040,190,1080], 'role':'green footer', 'mode':'#017950', 'median':[1,121,80]},
    ],
    'type_ink_measurement': {
        'method':'Approximate rotate-normalized coordinate v=round(y+0.077x), x45..810; count thresholded glyph pixels per v, retaining rows with >15 pixels. Ink spans are not font sizes.',
        'green_band_white_ink_px':34, 'yellow_band_green_ink_px':[37,38], 'white_band_green_ink_px':[48,37],
        'thresholds':'Hook min(R,G,B)>225 in v658..732; yellow R<65, 50<G<130, B<95 in v752..865; white R<65,50<G<145,B<100 in v886..1009.',
        'limits':'Antialiasing, accents, descenders, texture, imperfect rotation and lossy decoding affect spans; original CSS font sizes/weights remain unknown.'},
    'contrast': {'sampled_white_on_flat_green':5.45, 'note':'Reference yellow-ribbon text is visibly darker than flat ribbon green. Do not substitute #017950 for glyph ink or treat its imperfect filtered median as an official token. Final rendered text colors/contrast need verification.'},
    'missing_optional_measurement_tools':'Python fontTools unavailable; Pillow RAQM unavailable in this environment. No installation attempted. No Arabic shaping or copy-fit pass claimed.',
    'source_search_scope':'D:/Instagram plus this component. No matching original editable source located; does not rule out sources elsewhere or in Canva accounts.',
    'originals_unchanged':inventory['all_original_files_unchanged'],
    'not_performed':['template reconstruction','image generation','V4 export','mixed-script export QA','mobile creative export QA','form input/submission','matching/report generation','payment','publication','Creative02'],
}
(ROOT / 'analysis-review.json').write_text(json.dumps(review, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')

e = html.escape
def table(headers, rows):
    return '<table><thead><tr>'+''.join('<th>'+e(str(v))+'</th>' for v in headers)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+e(str(v))+'</td>' for v in row)+'</tr>' for row in rows)+'</tbody></table>'
group_table = table(['Famille','Références (préfixe imgi_)','Grammaire observée'], [(g['name'], ', '.join(map(str,g['ids'])),g['grammar']) for g in groups])
geometry_table = table(['Élément #32','Pixels source (864 × 1080)','Transposition 1080 × 1350'],[
    ('Logo, emprise visible estimée','x32, y30; 128 × 123','x40, y37.5; ≈160 × 154; garder le ratio naturel du fichier et ses marges transparentes'),
    ('Sujet visible estimé','x181–646, y153–1020; partie haute dégagée jusqu’à y630','Même ancre et recouvrement, ×1.25'),
    ('Ruban vert','Coins ≈(29,647),(819,586),(826,681),(35,742); épaisseur 96','Épaisseur ≈120; mêmes coins ×1.25'),
    ('Ruban jaune','Emprise x25–814, y686–876; épaisseur ≈132','Épaisseur ≈165; mêmes proportions'),
    ('Ruban blanc','Emprise x33–839, y814–1021; épaisseur ≈146','Épaisseur ≈182.5; mêmes proportions'),
    ('Inclinaison commune','≈−4.4°; bord droit plus haut','Conserver; aucun nouvel angle'),
    ('Footer','y1035, hauteur45; tab central x192–670 dès y1018','y1293.75, hauteur56.25; tab dès y1272.5'),
])
colors_table = table(['Rôle','Mesure source #32','Certitude'],[
    ('Vert ruban/footer','#017950 — RGB(1,121,80)','Mode/ médiane de zones plates; valeur encodée WebP, pas token officiel'),
    ('Jaune papier','#F9CB30 — RGB(249,203,48)','Zone plate; tonalités de papier à conserver'),
    ('Blanc intérieur du ruban','#FFFFFF','Pixels mesurés, bords gris/ombres distincts'),
    ('Papier clair','#EFEFEF mode; #EAEAEA médiane dans une zone libre','Texture et éclairage variables, pas un aplat unique'),
    ('Texte vert sur jaune','Vert plus foncé que le ruban; médiane filtrée ≈#115923','Échantillon descriptif imparfait, ne pas ériger en token exact'),
    ('Points/route','Menthe/vert pâle avec transparence','Pas de couleur uniforme récupérable sans calques originaux'),
])
slot_table = table(['Verrouillé après approbation','Remplaçable après approbation'],[
    ('Logo original, position et proportions','Hook, dans le ruban vert existant'),
    ('Fond papier, points, trajet, effets et ordre des calques','Promise, dans le ruban jaune existant'),
    ('Rubans: forme, angle, couleurs, chevauchement et marges','CTA, dans le ruban blanc existant, sans nouveau bouton'),
    ('Hiérarchie typographique; police/tailles/poids à identifier puis verrouiller','Image principale dans le cadre et le recadrage définis'),
    ('Cinq cadres circulaires, leurs positions, dimensions et ombres','Intérieur des cinq badges seulement si Imran valide cette variable'),
    ('Footer, icônes et contact historique','Aucune modification implicite du téléphone, domaine ou logo'),
])
items = lambda values: '<ul>'+''.join('<li>'+e(v)+'</li>' for v in values)+'</ul>'
content = f'''<!doctype html><html lang="fr"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>ProTrain — Analyse des références Instagram</title>
<style>body{{font:16px/1.6 system-ui,sans-serif;color:#17251f;background:#f3f3f1;margin:0}}main{{max-width:1160px;margin:auto;padding:32px}}h1{{font-size:30px}}h2{{margin-top:38px}}.notice{{background:#fff5cc;padding:20px;border-left:5px solid #756020}}table{{width:100%;border-collapse:collapse;background:white;margin:18px 0;font-size:14px}}td,th{{border:1px solid #d8ded9;padding:12px;text-align:left;vertical-align:top}}figure{{margin:24px 0}}img{{max-width:100%;height:auto;max-height:860px}}pre{{background:white;padding:20px;overflow:auto}}.copy{{direction:rtl;background:white;padding:18px;font-size:20px}}a{{color:#066443}}@media(max-width:700px){{main{{padding:18px}}table{{display:block;overflow-x:auto}}h1{{font-size:24px}}}}</style><main>
<p>PROTRAIN • 13 novembre 2026 • Analyse des sources, pas une nouvelle direction artistique</p><h1>Réutiliser l’identité Instagram existante</h1>
<p class="notice"><strong>Statut: proposition en attente d’Imran.</strong> Les phases d’analyse et de sélection sont terminées. Aucun template reconstruit, aucune image V4 générée ou exportée. Les 20 originaux sont inchangés par contrôle SHA-256.</p>
<h2>1. Design System Analysis</h2><p>Inspection de 20 fichiers locaux: 13 images de 864 × 1080, quatre de 881 × 1080, une de 1080 × 1350, une de 1080 × 1324 et une Story de 480 × 854. Les proportions ne sont donc pas toutes identiques. Les visuels fournis ont été examinés comme collection; #32 et #29 ont aussi été ouverts depuis les fichiers originaux.</p>
{group_table}
<p>Éléments récurrents: logo en haut à gauche, marges optiques plutôt qu’une grille de cartes, rubans de papier inclinés vers le haut à droite, vert/jaune/blanc, visage dégagé au-dessus des rubans et informations de contact en bas. Les photos plein cadre et les compositions papier sont deux familles distinctes. Un avion, des bulles ou une texture festive ne sont pas présents dans chaque référence et ne constituent pas un kit à accumuler.</p>
{colors_table}
<p>Les valeurs exactes du site (#0A6B43 et #F2A541, notamment) restent documentées dans le kit existant. Elles ne remplacent pas les couleurs observées dans la référence Instagram choisie. Aucun navy, mint proposé, bouton amber ou dégradé provenant d’une autre famille n’est ajouté.</p>
<p><strong>Typographie:</strong> sans géométrique arrondie, grasse, centrée et inclinée avec les rubans; footer plus petit et plus léger. Les noms de police, corps et graisses numériques restent inconnus. Poppins et Cairo sont documentés pour le site, pas certifiés pour ces posts. Mesure exploratoire de l’encre, après compensation approximative de l’angle: hook ≈34px de hauteur, deux lignes jaunes ≈37–38px, lignes blanches ≈37–48px, accents compris. Ce ne sont pas des corps typographiques. La distance entre les lignes jaunes est d’environ 57px. La référence possède un hook sur une ligne et deux lignes dans chacun des deux rubans suivants.</p>
<p><strong>CTA observé:</strong> aucun bouton SaaS récurrent dans cette collection. Le bas contient un footer de contact. Une phrase d’action peut reprendre un ruban existant; un nouveau bouton arrondi serait un écart au modèle.</p>
<h2>2. Une seule référence proposée: imgi_32</h2>
<figure><a href="{e(selected.as_uri())}"><img src="{e(selected.as_uri())}" alt="Original ProTrain imgi_32: étudiante hésitant entre plusieurs pays ou filières"></a><figcaption>Original intact • 864 × 1080 • «Tu as un problème d’orientation?» • aucun texte remplacé</figcaption></figure>
<p>Cette référence exprime déjà l’hésitation dans un choix d’études. Le sujet unique et les choix périphériques servent le message Campus France Confusion. Les rubans jaune et blanc disposent déjà de deux lignes, ce qui offre davantage de capacité que #34. #29 utilise des bulles de langue: sa grammaire ne sera pas fusionnée avec #32. Les scènes de conseiller, de diplôme ou de visa ne représentent pas directement l’outil Match.</p>
{geometry_table}
<p>Toutes les positions de contour sont des estimations visuelles, avec environ 5–12px d’incertitude sur les bords irréguliers. Les dimensions de fichier et échantillons RGB sont mesurés. Les cadres circulaires source occupent environ: Canada (128,174)–(189,231), UK (253,120)–(345,212), Italie (635,161)–(729,254), France (213,271)–(286,344), USA (605,321)–(686,403). Le passage au format demandé est une mise à l’échelle uniforme ×1.25.</p>
<h2>3. Fixed vs Variable</h2>{slot_table}
<p><strong>Variable de soutien proposée:</strong> les drapeaux représentent plusieurs pays. Pour une offre France uniquement, leur maintien est trompeur. Je propose de conserver exactement les cinq cadres et de remplacer uniquement leurs contenus par des choix académiques illustratifs, après validation. Aucun contenu de badge n’est choisi ou produit ici. Il ne s’agira jamais de vraies recommandations ni de résultats du produit.</p>
<h2>4. Structure réutilisable proposée</h2><p>Un fichier HTML/CSS ou SVG éditable avec calques séparés, plus un JSON de contenu validé. Une référence et une géométrie verrouillées; aucune sélection automatique de style et aucun mélange de familles.</p>
<pre>{e(chr(10).join(proposal['proposed_future_layers']))}</pre>
<p>Le mapping hook/vert, promise/jaune et CTA/blanc est une proposition adaptée à ce modèle, pas une règle universelle du framework. Le texte exact reste:</p>
<div class="copy"><p><strong>HOOK</strong><br><bdi>{e(proposal['variable_slots']['hook']['text'])}</bdi></p><p><strong>PROMISE</strong><br><bdi>{e(proposal['variable_slots']['promise']['text'])}</bdi></p><p><strong>CTA</strong><br><bdi>{e(proposal['variable_slots']['cta']['text'])}</bdi></p></div>
<p>Cette copie est affichée ici pour documenter le contenu, sans validation de sa composition visuelle. Le hook long peut dépasser la bande verte prévue pour une ligne. Après approbation, le préflight vérifiera les fragments arabes, les mots français LTR, la ponctuation et le nombre de lignes. Si les textes ne tiennent pas, aucune réduction automatique de police, modification du texte ou agrandissement de ruban: revenir à Imran avec l’écart concret.</p>
<p>Avant remplacement du contenu, reconstruire d’abord le modèle avec sa copie d’origine, puis le comparer à l’original côte à côte et par superposition. Après adaptation seulement: export 1080 × 1350, aperçu 360 × 450, contrôle de lecture réelle, contraste, contours, logo et conformité des variables. Aucun de ces contrôles d’un futur export n’est annoncé comme effectué aujourd’hui.</p>
<h2>5. Assets manquants et décisions avant production</h2>{items(proposal['unresolved'])}
<p>Disponible: logo corporate transparent fourni, 141 × 127px, avec marges transparentes; fichiers locaux Cairo et Poppins 600; anciens actifs de Creative01 conservés comme historique. La petite définition du logo limite la netteté d’un agrandissement. Les SVG existants sont des créations locales différentes, pas les sources Instagram. Aucune source Canva, PSD, AI ou SVG correspondant à ces posts n’a été retrouvée dans les deux périmètres locaux inspectés; cela ne prouve pas leur absence ailleurs.</p>
<p>Le footer est historiquement «+212 665423321 • www.protrain.ma». La destination actuelle Match documentée est sur protraincompany.com. Conserver sa géométrie est distinct de valider son contenu pour ce funnel. Toute mise à jour du contact, ajout du label produit Match ou modification de la grille nécessite une exception approuvée; rien n’a été changé.</p>
<p>La nouvelle promesse et le CTA suivent le brief propriétaire et l’inspection enregistrée de la landing: deux programmes gratuits après saisie du profil, rapport complet payant distinct. Les sorties n’ont pas été testées. Ne pas reprendre «jusqu’à l’admission», la gestion de dossier humaine ou d’autres promesses de l’ancien post pour Match.</p>
<h2>Preuves et arrêt demandé</h2><p><a href="inventory-measurements.json">Inventaire et couleurs</a> • <a href="reference-32-geometry.json">Géométrie source</a> • <a href="template-proposal.json">Proposition des calques et variables</a> • <a href="analysis-review.json">Revue et limites</a> • <a href="source-search-report.md">Recherche de sources originales</a></p>
<p><strong>À valider:</strong> la référence #32 comme modèle unique, les intérieurs des cinq badges comme variable, et les éventuelles exceptions concernant le footer, le label Match et la police arabe. La reconstruction et Creative01V4 attendent cette approbation. Aucun original, ancien PNG, campagne, site ou formulaire n’a été modifié. Aucune publication, dépense ou génération d’image.</p>
</main></html>'''
(ROOT / 'design-system-analysis.html').write_text(content, encoding='utf-8')
print(json.dumps({'report':str(ROOT/'design-system-analysis.html'), 'selected_reference_sha256':proposal['reference']['sha256'], 'reconstruction_performed':False},ensure_ascii=False))
