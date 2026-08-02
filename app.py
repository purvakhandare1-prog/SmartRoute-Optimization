from flask import Flask, render_template, request, redirect
import sqlite3
from tsp import tsp_dp

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/add-location", methods=["GET", "POST"])
def add_location():

    if request.method == "POST":

        name = request.form["name"]
        latitude = request.form["latitude"]
        longitude = request.form["longitude"]

        conn = sqlite3.connect("database/delivery.db")
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO locations(name, latitude, longitude) VALUES (?, ?, ?)",
            (name, latitude, longitude)
        )

        conn.commit()
        conn.close()

        return redirect("/locations")

    return render_template("add_location.html")


@app.route("/locations")
def locations():

    conn = sqlite3.connect("database/delivery.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM locations")

    data = cursor.fetchall()

    conn.close()

    return render_template("locations.html", locations=data)


@app.route("/delete-location/<int:id>")
def delete_location(id):

    conn = sqlite3.connect("database/delivery.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM locations WHERE id=?", (id,))

    conn.commit()
    conn.close()

    return redirect("/locations")


@app.route("/edit-location/<int:id>", methods=["GET", "POST"])
def edit_location(id):

    conn = sqlite3.connect("database/delivery.db")
    cursor = conn.cursor()

    if request.method == "POST":

        name = request.form["name"]
        latitude = request.form["latitude"]
        longitude = request.form["longitude"]

        cursor.execute("""
            UPDATE locations
            SET name=?, latitude=?, longitude=?
            WHERE id=?
        """, (name, latitude, longitude, id))

        conn.commit()
        conn.close()

        return redirect("/locations")

    cursor.execute("SELECT * FROM locations WHERE id=?", (id,))
    location = cursor.fetchone()

    conn.close()

    return render_template("edit_location.html", location=location)


@app.route("/dashboard")
def dashboard():

    conn = sqlite3.connect("database/delivery.db")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM locations")
    total_locations = cursor.fetchone()[0]

    conn.close()

    return render_template(
        "dashboard.html",
        total_locations=total_locations
    )


@app.route("/optimize")
def optimize():

    conn = sqlite3.connect("database/delivery.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM locations")

    locations = cursor.fetchall()

    conn.close()

    if len(locations) < 2:
        return "Please add at least 2 locations."

    distance, route, ordered_locations = tsp_dp(locations)

    return render_template(
        "result.html",
        distance=round(distance, 2),
        route=route,
        locations=ordered_locations
    )


if __name__ == "__main__":
    app.run(debug=True)