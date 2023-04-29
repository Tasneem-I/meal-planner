@app.route('/recipe_names', methods=["GET", "POST"])
def recipe_names():
    if request.method == "POST":
        name = request.form.get("name")
        complex = "https://api.spoonacular.com/recipes/complexSearch"
        params ={'apiKey': api_key,
                 'query': name,
                 'number' : 1} #REQUIRES CHANGE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        response = requests.get(complex, params=params)
        val = json.loads(response.text)
        meal_ids = [val["results"][i]["id"] for i in range(len(val["results"]))]
        titles = [val["results"][i]["title"] for i in range(len(val["results"]))]
        images = [val["results"][i]["image"] for i in range(len(val["results"]))]
        recipe_cards = []
        for i in meal_ids:
            place = "https://api.spoonacular.com/recipes/"+str(i)+"/card"
            param = {'apiKey' : api_key}
            results = requests.get(place, params=param)
            final = json.loads(results.text)
            card = final["url"]
            recipe_cards.append(card)
        
        return redirect(url_for("recipe_names",cards = recipe_cards))
    else:
        return render_template("recipes.html")