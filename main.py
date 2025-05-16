from flask import Flask, request, jsonify, render_template_string
from openai import OpenAI
import os

app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>CBAM Chat Assistant</title>
</head>
<body>
    <h2>Ask anything about CBAM reporting</h2>
    <form method="POST">
        <textarea name="prompt" rows="5" cols="60" placeholder="e.g. I export iron to Germany"></textarea><br>
        <button type="submit">Ask</button>
    </form>
    {% if response %}
    <h3>Response:</h3>
    <p>{{ response }}</p>
    {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def chatbot():
    response_text = ""
    if request.method == "POST":
        prompt = request.form["prompt"]
        try:
            chat_completion = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}]
            )
            response_text = chat_completion.choices[0].message.content
        except Exception as e:
            response_text = f"Error: {str(e)}"
    return render_template_string(HTML, response=response_text)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
