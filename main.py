from flask import Flask, request
import cohere
import os

app = Flask(__name__)

# Setup Cohere API
api_key = os.getenv("COHERE_API_KEY")
co = cohere.Client(api_key)

# Get response from Cohere
def ask_cohere(prompt):
    response = co.generate(
        model='command-r-plus',
        prompt=prompt,
        max_tokens=400,
        temperature=0.8
    )
    return response.generations[0].text.strip()

@app.route("/", methods=["GET", "POST"])
def home():
    html = """
    <body style="background-color: white; font-family: Arial, sans-serif; padding: 40px; text-align: center;">
        <div style="max-width: 600px; margin: auto; background-color: #f2f2f2; padding: 30px; 
                    border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1);">

            <h2 style="color: #003366;">🎓 Ascend AI 🚀</h2>
            <p style="color: #333;">Discover careers, skills and scholarships based on your interests</p>

            <form method="post">
                <label><b>Your Interest:</b></label><br>
                <input name="interest" placeholder="e.g. Data Science, Law" required 
                    style="padding: 8px; width: 90%; border: 1px solid #ccc; border-radius: 5px;"><br><br>

                <label><b>Choose Mode:</b></label><br>
                <input type="radio" name="mode" value="career" checked> Career Skill Builder<br>
                <input type="radio" name="mode" value="scholarship"> Scholarship Finder<br><br>

                <button type="submit" 
                    style="background-color: #0066cc; color: white; padding: 10px 20px; 
                           border: none; border-radius: 5px; font-size: 16px;">🔍 Submit</button>
            </form>
    """

    if request.method == "POST":
        interest = request.form.get("interest")
        mode = request.form.get("mode")
        if mode == "career":
            prompt = f"Suggest 3 careers, (required skills soft skills and hard skills), courses, companies: {interest}"
        else:
            prompt = f"List scholarships for: {interest} with eligibility and country including India and international scholarships"

        result = ask_cohere(prompt)

        
        html += f"""
           <b> <div style="font-family:   Arial, Helvetica, sans-serif; 
                        background-color: #e6f2ff; font-weight: 700; /* Bold */
color: #000000;   /* Black */
                        margin: 40px auto; 
                        padding: 25px; 
                        max-width: 800px;
                        border-radius: 10px; 
                        border: 1px solid #99ccff;
                        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);"> </b>

                <h3 style="color: #000000; font-size: 22px; margin-bottom: 15px;">✨ Result</h3>

                <pre style="white-space: pre-wrap; font-size: 16px; color: #333; line-height: 1.6; margin-bottom: 20px;">{result}</pre>

                <p style="color: #00000; font-size: 15px; margin-top: 10px;">
                    <b>🚀 Ascend today — because your future is worth planning!</b>
                </p>
            </div>
        """


    return html

app.run(host="0.0.0.0", port=3000)
