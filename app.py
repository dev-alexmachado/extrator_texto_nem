from flask import Flask, render_template, request
import easyocr


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


if __name__ == "__main__":
    app.run(debug=True)