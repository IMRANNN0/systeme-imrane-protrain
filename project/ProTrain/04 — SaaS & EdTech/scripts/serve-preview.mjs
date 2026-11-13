import http from 'node:http';
import fs from 'node:fs/promises';
const html = await fs.readFile(new URL('./SCRIPTS_CLIENT.html', import.meta.url));
http.createServer((req, res) => {
  if (req.url !== '/' && req.url !== '/SCRIPTS_CLIENT.html') { res.writeHead(404); res.end(); return; }
  res.writeHead(200, {'Content-Type':'text/html; charset=utf-8'});
  res.end(html);
}).listen(8765, '127.0.0.1', () => console.log('Preview ready at http://127.0.0.1:8765/SCRIPTS_CLIENT.html'));
