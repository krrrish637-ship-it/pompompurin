from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
import random

# SVG Vectorial de Pompompurin
POMPOMPURIN_NORMAL = '''
<svg width="140" height="130" viewBox="0 0 200 180" xmlns="http://www.w3.org/2000/svg">
  <ellipse cx="40" cy="90" rx="25" ry="40" fill="#FFE57F" transform="rotate(20 40 90)"/>
  <ellipse cx="160" cy="90" rx="25" ry="40" fill="#FFE57F" transform="rotate(-20 160 90)"/>
  <ellipse cx="100" cy="100" rx="75" ry="60" fill="#FFE57F"/>
  <path d="M 75 45 Q 100 25 125 45 Z" fill="#6D4C41"/>
  <rect x="96" y="23" width="8" height="10" rx="3" fill="#6D4C41"/>
  <circle cx="75" cy="95" r="6" fill="#4E342E"/>
  <circle cx="125" cy="95" r="6" fill="#4E342E"/>
  <ellipse cx="100" cy="102" rx="5" ry="4" fill="#4E342E"/>
  <path d="M 93 108 Q 100 116 107 108" stroke="#4E342E" stroke-width="3" fill="none" stroke-linecap="round"/>
  <ellipse cx="60" cy="108" rx="10" ry="6" fill="#FF8A80" opacity="0.6"/>
  <ellipse cx="140" cy="108" rx="10" ry="6" fill="#FF8A80" opacity="0.6"/>
</svg>
'''

POMPOMPURIN_TRISTE = '''
<svg width="140" height="130" viewBox="0 0 200 180" xmlns="http://www.w3.org/2000/svg">
  <ellipse cx="35" cy="105" rx="22" ry="38" fill="#FFE57F" transform="rotate(35 35 105)"/>
  <ellipse cx="165" cy="105" rx="22" ry="38" fill="#FFE57F" transform="rotate(-35 165 105)"/>
  <ellipse cx="100" cy="100" rx="75" ry="60" fill="#FFE57F"/>
  <path d="M 75 45 Q 100 25 125 45 Z" fill="#6D4C41"/>
  <rect x="96" y="23" width="8" height="10" rx="3" fill="#6D4C41"/>
  <path d="M 68 93 Q 75 99 82 93" stroke="#4E342E" stroke-width="3" fill="none" stroke-linecap="round"/>
  <path d="M 118 93 Q 125 99 132 93" stroke="#4E342E" stroke-width="3" fill="none" stroke-linecap="round"/>
  <path d="M 60 102 Q 60 112 65 112 Q 70 112 70 102 Q 65 95 60 102 Z" fill="#4FC3F7"/>
  <ellipse cx="100" cy="102" rx="5" ry="4" fill="#4E342E"/>
  <path d="M 93 114 Q 100 107 107 114" stroke="#4E342E" stroke-width="3" fill="none" stroke-linecap="round"/>
</svg>
'''

POMPOMPURIN_FELIZ = '''
<svg width="140" height="130" viewBox="0 0 200 180" xmlns="http://www.w3.org/2000/svg">
  <ellipse cx="45" cy="75" rx="22" ry="38" fill="#FFE57F" transform="rotate(-10 45 75)"/>
  <ellipse cx="155" cy="75" rx="22" ry="38" fill="#FFE57F" transform="rotate(10 155 75)"/>
  <ellipse cx="100" cy="100" rx="75" ry="60" fill="#FFE57F"/>
  <path d="M 75 45 Q 100 25 125 45 Z" fill="#6D4C41"/>
  <rect x="96" y="23" width="8" height="10" rx="3" fill="#6D4C41"/>
  <path d="M 68 95 Q 75 85 82 95" stroke="#4E342E" stroke-width="4" fill="none" stroke-linecap="round"/>
  <path d="M 118 95 Q 125 85 132 95" stroke="#4E342E" stroke-width="4" fill="none" stroke-linecap="round"/>
  <path d="M 100 120 C 100 115, 90 110, 90 120 C 90 127, 100 133, 100 135 C 100 133, 110 127, 110 120 C 110 110, 100 115, 100 120 Z" fill="#FF5252"/>
  <ellipse cx="60" cy="105" rx="12" ry="7" fill="#FF8A80" opacity="0.7"/>
  <ellipse cx="140" cy="105" rx="12" ry="7" fill="#FF8A80" opacity="0.7"/>
</svg>
'''

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pregunta Especial 🌸 Pompompurin 💖</title>
    <style>
        body {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #FFE5EC;
            text-align: center;
            color: #B56576;
            overflow: hidden;
            position: relative;
        }

        .decoracion-fondo {
            position: absolute;
            font-size: 2rem;
            opacity: 0.25;
            user-select: none;
        }

        .card {
            background-color: #ffffff;
            padding: 30px;
            border-radius: 20px;
            box-shadow: 0 8px 20px rgba(181, 101, 118, 0.2);
            text-align: center;
            max-width: 400px;
            width: 85%;
            border: 4px solid #FFCAD4;
            z-index: 10;
            position: relative;
            min-height: 250px;
        }

        h1 {
            color: #B56576;
            font-size: 1.8rem;
            margin: 10px 0 25px 0;
        }

        .contenedor-botones {
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 15px;
            margin-top: 20px;
            position: relative;
        }

        .btn {
            padding: 10px 25px;
            font-size: 1.1rem;
            font-weight: bold;
            border-radius: 50px;
            text-decoration: none;
            display: inline-block;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05);
            transition: transform 0.2s;
        }

        .btn-yes {
            background-color: #FFB7B2;
            color: #ffffff;
        }

        .btn-no-fijo {
            background-color: #FFDAC1;
            color: #B56576;
        }

        .btn-no-movil {
            background-color: #FFDAC1;
            color: #B56576;
            position: absolute;
            top: POS_Ypx;
            left: POS_Xpx;
        }
    </style>
</head>
<body>

    <div class="decoracion-fondo" style="top: 10%; left: 10%;">🌸</div>
    <div class="decoracion-fondo" style="top: 20%; right: 15%;">💖</div>
    <div class="decoracion-fondo" style="bottom: 15%; left: 20%;">❁</div>
    <div class="decoracion-fondo" style="bottom: 10%; right: 10%;">💕</div>
    <div class="decoracion-fondo" style="top: 50%; left: 5%;">🌷</div>

    <div class="card">
        CONTENIDO_DINAMICO
    </div>

</body>
</html>
'''

class MiServidor(BaseHTTPRequestHandler):
    def do_GET(self):
        url_parseada = urlparse(self.path)
        parametros = parse_qs(url_parseada.query)
        
        estado = parametros.get('estado', ['inicio'])[0]
        opcion = parametros.get('opcion', [None])[0]

        pos_x = random.randint(20, 260)
        pos_y = random.randint(10, 50)

        if estado == 'inicio':
            if opcion == 'no':
                nuevo_estado = 'seguro'
                titulo = '¿Estás seguro? 🥺'
                svg_pompompurin = POMPOMPURIN_NORMAL
                es_movil = False
            elif opcion == 'si':
                nuevo_estado = 'final'
            else:
                nuevo_estado = 'inicio'
                titulo = '¿Me amas? 💌'
                svg_pompompurin = POMPOMPURIN_NORMAL
                es_movil = False

        elif estado == 'seguro':
            if opcion == 'si':
                nuevo_estado = 'triste'
                titulo = '¿Me amas? 😥'
                svg_pompompurin = POMPOMPURIN_TRISTE
                es_movil = True
            else:
                nuevo_estado = 'seguro'
                titulo = '¿Estás seguro? 🥺'
                svg_pompompurin = POMPOMPURIN_NORMAL
                es_movil = False

        elif estado == 'triste':
            if opcion == 'si':
                nuevo_estado = 'final'
            else:
                nuevo_estado = 'triste'
                titulo = '¿Me amas? 😥'
                svg_pompompurin = POMPOMPURIN_TRISTE
                es_movil = True

        if estado == 'final' or (opcion == 'si' and estado in ['inicio', 'triste']):
            contenido = f'''
                {POMPOMPURIN_FELIZ}
                <h1>¡Yo te amo más! 💖</h1>
                <p style="font-size: 1.4rem;">🌸 💕 ❁ 💕 🌸</p>
            '''
        else:
            clase_no = "btn-no-movil" if es_movil else "btn-no-fijo"
            contenido = f'''
                {svg_pompompurin}
                <h1>{titulo}</h1>
                <div class="contenedor-botones">
                    <a href="/?estado={nuevo_estado}&opcion=si" class="btn btn-yes">Sí 💖</a>
                    <a href="/?estado={nuevo_estado}&opcion=no" class="btn {clase_no}">No 💔</a>
                </div>
            '''

        html_final = HTML_TEMPLATE.replace('CONTENIDO_DINAMICO', contenido)
        html_final = html_final.replace('POS_X', str(pos_x))
        html_final = html_final.replace('POS_Y', str(pos_y))

        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html_final.encode('utf-8'))

if __name__ == '__main__':
    servidor = HTTPServer(('localhost', 8000), MiServidor)
    print("Servidor listo en http://localhost:8000")
    servidor.serve_forever()
