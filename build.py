# Gera index.html autocontido (imagens em base64, cada uma 1 vez) a partir de src.html + img/
import re, base64, json, os, sys
root = sys.argv[1]
s = open(os.path.join(root, 'src.html'), encoding='utf-8').read()
keys = sorted(set(re.findall(r'src="img/(\w+)\.webp"', s)))
m = {k: 'data:image/webp;base64,' + base64.b64encode(open(os.path.join(root, 'img', k + '.webp'), 'rb').read()).decode() for k in keys}
s = re.sub(r'src="img/(\w+)\.webp"', r'data-k="\1"', s)
fill = "<script>document.querySelectorAll('img[data-k]').forEach(function(i){if(!i.src)i.src=__IMG[i.dataset.k]})</script>"
s = s.replace("<script>document.documentElement.classList.add('js')</script>",
              "<script>document.documentElement.classList.add('js');window.__IMG=" + json.dumps(m) + "</script>", 1)
s = s.replace('</header>', '</header>\n' + fill, 1)
s = s.replace('<script>\n(() => {', fill + '\n<script>\n(() => {', 1)
open(os.path.join(root, 'index.html'), 'w', encoding='utf-8').write(s)
print('index.html', os.path.getsize(os.path.join(root, 'index.html')) // 1024, 'KB', len(keys), 'imagens')
