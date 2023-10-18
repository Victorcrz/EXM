from flask import Flask, request, render_template
import openai

app = Flask(__name__)
openai.api_key = "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"
img = []

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == 'POST':
        descripcion = request.form.get("descripcion")
        creaimg = int(request.form.get("creaimg"))
        for _ in range(creaimg):
            url_img = crear_img(descripcion)
            img.append(url_img)
        reschat = generar_res(descripcion)
        return render_template('index.html', img=img, reschat=reschat)
    return render_template('index.html', img=img)

def crear_img(descripcion):
    respuesta = openai.Image.create(
            prompt=descripcion,
            n=1,
            size="256x256"
        )
    return respuesta["data"][0]["url"]

def generar_res(descripcion):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": descripcion
            }
        ]
    )

    respuesta_chat = response["choices"][0]["message"]["content"]

    return respuesta_chat

if __name__ == "__main__":
    app.run(debug=True, port=5000)