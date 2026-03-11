from flask import Flask, request, render_template_string
import pandas as pd
import os
import re

app = Flask(__name__)

file_name = "password_data.xlsx"

# Create excel if not exists
if not os.path.exists(file_name):
    df = pd.DataFrame(columns=["Username","Password","Strength"])
    df.to_excel(file_name,index=False)


def check_strength(password):

    if len(password) >= 8 and re.search("[A-Z]",password) and re.search("[0-9]",password) and re.search("[@#$%^&*!]",password):
        return "Strong"
    elif len(password) >= 6:
        return "Medium"
    else:
        return "Weak"


HTML = """
<!DOCTYPE html>
<html>
<head>
<title>Password Strength Checker</title>

<style>
body{
font-family:Arial;
background:#0f172a;
color:white;
display:flex;
justify-content:center;
align-items:center;
height:100vh;
}

.container{
background:#1e293b;
padding:40px;
border-radius:12px;
width:320px;
text-align:center;
}

input{
width:90%;
padding:12px;
margin:10px;
border:none;
border-radius:6px;
}

button{
padding:10px 20px;
background:#38bdf8;
border:none;
color:white;
border-radius:6px;
cursor:pointer;
}

</style>
</head>

<body>

<div class="container">

<h2>Password Strength Checker</h2>

<form method="POST">

<input type="text" name="username" placeholder="Enter Username" required>

<input type="password" name="password" placeholder="Enter Password" required>

<button type="submit">Check</button>

</form>

{% if strength %}
<h3>Password Strength: {{strength}}</h3>
{% endif %}

</div>

</body>
</html>
"""


@app.route("/",methods=["GET","POST"])
def home():

    strength=""

    if request.method=="POST":

        username=request.form["username"]
        password=request.form["password"]

        strength=check_strength(password)

        df=pd.read_excel(file_name)

        new_row={
        "Username":username,
        "Password":password,
        "Strength":strength
        }

        df=pd.concat([df,pd.DataFrame([new_row])],ignore_index=True)

        df.to_excel(file_name,index=False)

    return render_template_string(HTML,strength=strength)


if __name__=="__main__":
    app.run(debug=True)