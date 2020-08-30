from cs50 import SQL
from flask import Flask, redirect, request, render_template

app = Flask(__name__)

db = SQL("sqlite:///members.db")

@app.route("/")
def index():
    rows = db.execute("SELECT * FROM members")
    return render_template("index.html", rows=rows)

@app.route("/insert", methods=["GET", "POST"])
def insert():
    if request.method == "GET":
        return render_template("insert.html")
    else:
        name = request.form.get("name")
        if not name:
            return render_template("apology.html", message="Você precisa colocar um nome.")
        email = request.form.get("email")
        if not email:
            return render_template("apology.html", message="Você precisa colocar um email.")
        address = request.form.get("address")
        if not address:
            return render_template("apology.html", message="Você precisa colocar um endereço.")
        phone = request.form.get("phone")
        if not phone:
            return render_template("apology.html", message="Você precisa colocar um telefone.")
        db.execute("INSERT INTO members (name, email, address, phone) VALUES (:name, :email, :address, :phone)", name=name, email=email, address=address, phone=phone)
        return redirect("/")


@app.route("/edit", methods=["GET", "POST"])
def edit():
    if request.method == "GET":
        id= request.args.get("id")
        member = db.execute("SELECT id, name, email, address, phone FROM members WHERE id = :id", id=id)
        if not member:
            return render_template("apology.html", message="Erro encontrado.")
        return render_template("edit.html", member = member[0])
    else:
        id= request.form.get("id")
        name = request.form.get("name")
        if not name:
            return render_template("apology.html", message="Você precisa colocar um nome.")
        email = request.form.get("email")
        if not email:
            return render_template("apology.html", message="Você precisa colocar um email.")
        address = request.form.get("address")
        if not address:
            return render_template("apology.html", message="Você precisa colocar um endereço.")
        phone = request.form.get("phone")
        if not phone:
            return render_template("apology.html", message="Você precisa colocar um telefone.")
        db.execute("UPDATE members SET name=:name, email=:email, address=:address, phone=:phone WHERE id=:id ", name=name, email=email, address=address, phone=phone, id=id)
        return redirect("/")

@app.route("/delete", methods=["GET", "POST"])
def delete():
    if request.method == "GET":
        id = request.args.get("id")
        member = db.execute("SELECT id, name, email, address, phone FROM members WHERE id = :id", id=id)
        return render_template("delete.html", member = member[0])
    else:
        id = request.form.get("id")
        db.execute("DELETE FROM members WHERE id=:id", id=id)
        return redirect("/")