from flask import Flask, render_template, request, flash, redirect, abort
from InputForm import InputForm
import secrets

app = Flask(__name__)
app.config['SECRET_KEY'] = "abc"

shortened_urls = []

@app.route("/", methods=["GET", "POST"])
def home():
    form = InputForm()
    if request.method == "POST":
        if form.validate_on_submit():
            id = secrets.token_urlsafe(8)
            shortened_url = request.base_url + id
            shortened_urls.append({"destination_url": form.url.data, "id": id})
            flash(f"Shortened URL: {shortened_url}", "success message")
            form.url.data=''
        else:
            flash("Invalid URL!", "error message")
    return render_template("index.html", form=form)

@app.route("/<id>")
def shortened(id):
    for shortened_url in shortened_urls:
        if shortened_url["id"] == id:
            return redirect(shortened_url["destination_url"])
    return abort(404)

if __name__ == "__main__":
    app.run(debug=True)