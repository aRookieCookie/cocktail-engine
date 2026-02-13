from flask import Flask, render_template, request
import requests

app = Flask(__name__)

cocktail_dict = {
    "strDrink": " Margarita",
    "strCategory": "Ordinary Drink",
    "strAlcoholic": "Alcoholic",
    "strGlass": "Cocktail glass",
    "strInstructions": "Rub the rim of the glass with the lime slice to make the salt stick to it. Take care to moisten only the outer rim and sprinkle the salt on it. The salt should present to the lips of the imbiber and never mix into the cocktail. Shake the other ingredients with ice, then carefully pour into the glass.",
    "strDrinkThumb": "https://www.thecocktaildb.com/images/media/drink/5noda61589575158.jpg",
    "strIngredient1": "Tequila",
    "strIngredient2": "Triple sec",
    "strIngredient3": "Lime juice",
    "strIngredient4": "Salt",
    "strIngredient5": "null",
    "strMeasure1": "1 1/2 oz ",
    "strMeasure2": "1/2 oz ",
    "strMeasure3": "1 oz ",
    "strMeasure4": "null",
    "strMeasure5": "null",
}
errormsg = "Found No Drinks!"
base_url = "https://www.thecocktaildb.com/api/json/v1/1/"

def get_result(query, type, isalcoholic):
    if type == "name":
        op = "search.php?s="
    elif type == "ingredient":
        op = "search.php?i="
    elif type == "id":
        op = "lookup.php?i="
        
    url = base_url+op+query
    response = requests.get(url)
    data = response.json()
    if data["drinks"] is None:
        return {"drinks": []}
    else:
        data = parse_data(data)
    return data
    
def parse_data(data):
    parsed_data = {"drinks" : []}

    for i in range(len(data["drinks"])):
        cd = data["drinks"][i]
        current_drink = {
            "name" : cd["strDrink"],
            "category" : cd["strCategory"],
            "instructions" : cd["strInstructions"],
            "image" : cd["strDrinkThumb"],
            "ingredients" : [cd[f"strIngredient{i}"] for i in range(1, 16) if cd[f"strIngredient{i}"]],
            "measures" : [cd[f"strMeasure{i}"] for i in range(1, 16) if cd[f"strIngredient{i}"]],
            "isAlcoholic": cd["strAlcoholic"],
            "id": cd["idDrink"]
        }
        parsed_data["drinks"].append(current_drink)
    return parsed_data

@app.route("/")
def index():
    # Check if 'name' is in the URL (e.g., /?name=Margarita)
    name_query = request.args.get('name')
    isalcoholic = request.args.get('isAlcoholic')
    if name_query:
        result = get_result(name_query, "name", isalcoholic)
        return render_template("index.html", result=result)
    
    # Otherwise, just show the normal homepage
    return render_template("index.html", result="No Results")

@app.route("/", methods=['POST'])
def openDrink():
    if request.method == 'POST':
        id = request.form['id']
        drink = get_result(id , "id", True)
        return render_template("drink.html", drink=drink)

app.run(host="0.0.0.0", port=80, debug=True)
