from flask import Flask, request, render_template_string
from openai import OpenAI
import os

app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>CBAM Chat Assistant</title>
</head>
<body>
    <h2>Ask anything about CBAM reporting</h2>
    <form method="post">
        <textarea name="user_input" rows="4" cols="60" placeholder="e.g. I export iron to Germany">{{ user_input }}</textarea><br>
        <button type="submit">Ask</button>
    </form>
    <h4>Response:</h4>
    <p>{{ response }}</p>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def chat():
    response_text = ""
    user_input = ""

    if request.method == "POST":
        user_input = request.form["user_input"]
        try:
            completion = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant for CBAM (Carbon Border Adjustment Mechanism) regulations."},
                    {"role": "user", "content": user_input}
                ]
            )
            response_text = completion.choices[0].message.content.strip()
        except Exception as e:
            response_text = f"Error: {str(e)}"

    return render_template_string(HTML_TEMPLATE, response=response_text, user_input=user_input)

if __name__ == "__main__":
    app.run(debug=True, port=10000)
