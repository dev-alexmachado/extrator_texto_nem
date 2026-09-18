from flask import Flask, render_template, request, send_file
from translate import Translator
import easyocr

import io


app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/extrair", methods = ['POST'])
def extrair():
    if 'imagem' not in request.files:
        return "Nenhuma imagem enviada", 400
    imagem = request.files['imagem']
    if imagem.filename == '':
        return "Nenhuma imagem selecionada", 400
    render = easyocr.Reader(['en','pt'], gpu=False)
    result = render.readtext(imagem.read())
    texto_extraido = ' '.join([res[1] for res in result])
    return render_template("extracao.html", texto=texto_extraido)

@app.route("/salvarTexto", methods = ['POST'])
def salvar_texto():
    if request.method == "POST":
        texto = request.form.get("texto", "")
        arquivo_buffer = io.BytesIO(texto.encode('utf-8'))
        
        return send_file(
            arquivo_buffer,
            mimetype='text/plain',
            as_attachment=True,
            download_name='seu_arquivo.txt'
        )
    
    return render_template("salvar_sucesso.html")

@app.route("/traducao", methods = ['POST'])
def traduzir():
    tradutor = Translator(to_lang="pt")
    texto_traduzido = None
    if request.method == "POST":
        texto = request.form.get("texto","")
        texto_traduzido = tradutor.translate(texto)
    return render_template("extracao.html")


if __name__ == "__main__":
    app.run(debug=True)