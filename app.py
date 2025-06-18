from flask import Flask, redirect, request, render_template
from db.contact import ContactDB
from model.contact import Contact

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

db = ContactDB("data/contacts.csv")


@app.route("/")
def index():
    return redirect("/contacts")


@app.route("/contacts", methods=["GET"])
def contacts():
    search = request.args.get("q")
    if search is not None:
        contacts_set = db.search(search)
    else:
        contacts_set = db.all()
    return render_template("index.html", contacts=contacts_set)


@app.route("/contacts/new", methods=["GET"])
def contacts_new_get():
    return render_template("new_contact.html", contact=Contact())


@app.route("/contacts/new", methods=["POST"])
def contacts_new_post():
    new_contact = Contact(
        None,
        request.form["first_name"],
        request.form["last_name"],
        request.form["phone"],
        request.form["email"],
    )
    if db.create(new_contact):
        return redirect("/contacts")
    else:
        return render_template("new_contact.html", contact=new_contact)


@app.route("/contacts/<int:contact_id>", methods=["GET"])
def contacts_view(contact_id=0):
    contact = db.find(contact_id)
    return render_template("contact.html", contact=contact)


@app.route("/contacts/<int:contact_id>/edit", methods=["GET"])
def contacts_edit_get(contact_id=0):
    contact = db.find(contact_id)
    return render_template("edit_contact.html", contact=contact)


@app.route("/contacts/<int:contact_id>/edit", methods=["POST"])
def contacts_edit_post(contact_id=0):
    updated_contact = Contact(
        contact_id,
        request.form["first_name"],
        request.form["last_name"],
        request.form["phone"],
        request.form["email"],
    )
    if db.update(updated_contact):
        return redirect(f"/contacts/{contact_id}")
    else:
        return render_template("edit_contact.html", contact=updated_contact)


@app.route("/contacts/<int:contact_id>", methods=["DELETE"])
def contact_delete(contact_id=0):
    db.delete(contact_id)
    return redirect("/contacts", 303)


if __name__ == "__main__":
    app.run(port=7777, debug=True)
