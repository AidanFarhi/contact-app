from flask import Flask, redirect, request, render_template
from db.contact import ContactDB
from model.contact import Contact

app = Flask(__name__)

db = ContactDB("data/contacts.csv")


@app.route("/")
def index():
    return redirect("/contacts")


@app.route("/contacts")
def contacts():
    search = request.args.get("q")
    if search is not None:
        contacts_set = db.search(search)
    else:
        contacts_set = db.all()
    return render_template("index.html", contacts=contacts_set)


@app.route("/contacts/new", methods=["GET"])
def contacts_new_get():
    return render_template("new_contact_form.html", contact=Contact())


@app.route("/contacts/new", methods=["POST"])
def contacts_new():
    new_contact = Contact(
        request.form["first_name"],
        request.form["last_name"],
        request.form["phone"],
        request.form["email"],
    )
    if db.create(new_contact):
        return redirect("/contacts")
    else:
        return render_template("new.html", contact=new_contact)


if __name__ == "__main__":
    app.run(port=7777, debug=True)
