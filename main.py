from flask import Flask, request, render_template_string
import openai
import os

app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
  <head>
    <title>CBAM Chat Assistant</title>
  </head>
  <body style="font-family: sans-serif; padding: 40px;">
    <h2>Ask anything about CBAM reporting</h2>
    <form method="POST">
      <textarea name="message" rows="6" cols="60" placeholder="e.g. I export iron to Germany"></textarea><br><br>
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
def index():
    response_text = ""
    if request.method == "POST":
        user_input = request.form["message"]
        try:
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert assistant helping exporters with CBAM (Carbon Border Adjustment Mechanism) reporting. Be very clear and helpful. Always adapt to the user's language."},
                    {"role": "user", "content": user_input}
                ]
            )
            response_text = completion.choices[0].message["content"]
        except Exception as e:
            response_text = f"Error: {str(e)}"

    return render_template_string(HTML_TEMPLATE, response=response_text)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
