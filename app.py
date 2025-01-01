from flask import Flask, render_template, request
import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

db = SQL("sqlite:///schedule.db")

def apology(message):
     return render_template("apology.html", message=message)

stafferCurrent = 1

perShift = 0

@app.route("/")
def index():
    name = request.args.get("name", "world")
    return render_template("welcome.html", name=name)

# CREATE TABLE schedules (name TEXT NOT NULL, hash TEXT NOT NULL, timestamp DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP)
# CREATE TABLE staffers (name TEXT NOT NULL, shifts NUMERIC NOT NULL DEFAULT 0, monday INT, tuesday INT, wednesday INT,
# thursday INT, friday INT, saturday INT, sunday INT);

@app.route("/new", methods=["GET", "POST"])
def new():
     global perShift
     if request.method == "GET":
            return render_template("new.html")
     else:
        # check for valid inputs
        # check total number of staffers
        if not request.form.get("staffersNum"):
             return apology("must enter a quantity of staffers")
        if request.form.get("staffersNum").isnumeric() == False:
             return apology("must enter a positive integer value for staffers")
        staffers = int(request.form.get("staffersNum"))
        if staffers == 0:
             return apology("must enter a nonzero integer value for staffers")
        # check number of staffers per shift
        if not request.form.get("perShift"):
             return apology("must enter a quantity of staffers per day")
        if request.form.get("perShift").isnumeric() == False:
             return apology("must enter a positive integer value for staffers per day")
        perShift = int(request.form.get("perShift"))
        if perShift == 0:
             return apology("must enter a nonzero integer value for staffers per day")

        # insert new schedule info into schedules table
        db.execute(
            "INSERT INTO dimensions (weeks, staffers, perShift) VALUES (?, ?, ?)",
            request.form.get("weeks"),
            staffers,
            perShift)

        global stafferCurrent
        stafferCurrent = 1
        db.execute("DELETE FROM staffers")

        return redirect("/staffers")


@app.route("/staffers", methods=["GET", "POST"])
def staffers():
     global stafferCurrent
     length = len(db.execute("SELECT * FROM dimensions"))
     staffersRows = db.execute("SELECT staffers FROM dimensions WHERE id = ?", length)
     staffers = int(staffersRows[0]['staffers'])
     staffersPerRows = db.execute("SELECT perShift FROM dimensions WHERE id = ?", length)
     staffersPer = int(staffersPerRows[0]['perShift'])
     if request.method == "GET":
          return render_template("staffers.html", staffers=staffers, stafferCurrent=stafferCurrent)
     else:
               # check for name
          if not request.form.get("stafferName"):
               return apology("must input a name")
               # check for seven radios
          if not (request.form.get("sunday") and
                  request.form.get("monday") and
                  request.form.get("tuesday") and
                  request.form.get("wednesday") and
                  request.form.get("thursday") and
                  request.form.get("friday") and
                  request.form.get("saturday")):
               return apology("must input availability for each day")

               # input staffer's data into new table
          db.execute("INSERT INTO staffers (name, monday, tuesday, wednesday, thursday, friday, saturday, sunday) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                         request.form.get("stafferName"), request.form.get("monday"), request.form.get("tuesday"), request.form.get("wednesday"),
                         request.form.get("thursday"), request.form.get("friday"), request.form.get("saturday"), request.form.get("sunday"))

          if stafferCurrent < staffers:
               stafferCurrent += 1
               return render_template("staffers.html", staffers=staffers, staffersPer=staffersPer, stafferCurrent=stafferCurrent)
          else:
               db.execute("DELETE FROM output")
               return redirect("/output")


# CREATE TABLE output (sunday TEXT NOT NULL, monday TEXT NOT NULL, tuesday TEXT NOT NULL, wednesday TEXT NOT NULL,
# thursday TEXT NOT NULL, friday TEXT NOT NULL, saturday TEXT NOT NULL, rowId INTEGER AUTOINCREMENT)

@app.route("/output", methods=["GET", "POST"])
def output():
     if request.method == "GET":
          # generate "empty" table
          global perShift
          rows = perShift
          while perShift > 0:
               db.execute("INSERT INTO output (sunday, monday, tuesday, wednesday, thursday, friday, saturday, rowId) VALUES (0, 0, 0, 0, 0, 0, 0, ?)", perShift)
               perShift -= 1

          for x in range(1, rows + 1):

               availableMonRows = db.execute("SELECT name FROM staffers WHERE monday = 1 AND moBool = 0 ORDER BY shifts ASC")
               preferNotMonRows = db.execute("SELECT name FROM staffers WHERE monday = 2 AND moBool = 0 ORDER BY shifts ASC")
               if len(availableMonRows) > 0:
                    # update the output table with the name of the available person
                    db.execute("UPDATE output SET monday = ? WHERE rowId = ?", availableMonRows[0]['name'], x)
                    # update the person's shift count
                    countRow = db.execute("SELECT shifts FROM staffers WHERE name = ?", availableMonRows[0]['name'])
                    count = countRow[0]['shifts']
                    db.execute("UPDATE staffers SET shifts = ?, moBool = 1 WHERE name = ?", count + 1, availableMonRows[0]['name'])
               elif len(preferNotMonRows) > 0:
                    # select prefer-not-tos
                    db.execute("UPDATE output SET monday = ? WHERE rowId = ?", preferNotMonRows[0]['name'], x)
                    # update the person's shift count
                    countRow = db.execute("SELECT shifts FROM staffers WHERE name = ?", preferNotMonRows[0]['name'])
                    count = countRow[0]['shifts']
                    db.execute("UPDATE staffers SET shifts = ?, moBool = 1 WHERE name = ?", count + 1, preferNotMonRows[0]['name'])
               else:
                    # return message saying nobody available mon
                    db.execute("UPDATE output SET monday = ? WHERE rowId = ?", 'UNFILLED', x)

               availableTuesRows = db.execute("SELECT name FROM staffers WHERE tuesday = 1 AND tuBool = 0 ORDER BY shifts ASC")
               preferNotTuesRows = db.execute("SELECT name FROM staffers WHERE tuesday = 2 AND tuBool = 0 ORDER BY shifts ASC")
               if len(availableTuesRows) > 0:
                    # update the output table with the name of the available person
                    db.execute("UPDATE output SET tuesday = ? WHERE rowId = ?", availableTuesRows[0]['name'], x)
                    # update the person's shift count
                    countRow = db.execute("SELECT shifts FROM staffers WHERE name = ?", availableTuesRows[0]['name'])
                    count = countRow[0]['shifts']
                    db.execute("UPDATE staffers SET shifts = ?, tuBool = 1 WHERE name = ?", count + 1, availableTuesRows[0]['name'])
               elif len(preferNotTuesRows) > 0:
                    # select prefer-not-tos
                    db.execute("UPDATE output SET tuesday = ? WHERE rowId = ?", preferNotTuesRows[0]['name'], x)
                     # update the person's shift count
                    countRow = db.execute("SELECT shifts FROM staffers WHERE name = ?", preferNotTuesRows[0]['name'])
                    count = countRow[0]['shifts']
                    db.execute("UPDATE staffers SET shifts = ?, tuBool = 1 WHERE name = ?", count + 1, preferNotTuesRows[0]['name'])
               else:
                    # return message saying nobody available mon
                    db.execute("UPDATE output SET tuesday = ? WHERE rowId = ?", 'UNFILLED', x)

               availableWedRows = db.execute("SELECT name FROM staffers WHERE wednesday = 1 AND weBool = 0 ORDER BY shifts ASC")
               preferNotWedRows = db.execute("SELECT name FROM staffers WHERE wednesday = 2 AND weBool = 0 ORDER BY shifts ASC")
               if len(availableWedRows) > 0:
                    # update the output table with the name of the available person
                    db.execute("UPDATE output SET wednesday = ? WHERE rowId = ?", availableWedRows[0]['name'], x)
                    # update the person's shift count
                    countRow = db.execute("SELECT shifts FROM staffers WHERE name = ?", availableWedRows[0]['name'])
                    count = countRow[0]['shifts']
                    db.execute("UPDATE staffers SET shifts = ?, weBool = 1 WHERE name = ?", count + 1, availableWedRows[0]['name'])
               elif len(preferNotWedRows) > 0:
                    # select prefer-not-tos
                    db.execute("UPDATE output SET wednesday = ? WHERE rowId = ?", preferNotWedRows[0]['name'], x)
                     # update the person's shift count
                    countRow = db.execute("SELECT shifts FROM staffers WHERE name = ?", preferNotWedRows[0]['name'])
                    count = countRow[0]['shifts']
                    db.execute("UPDATE staffers SET shifts = ?, weBool = 1 WHERE name = ?", count + 1, preferNotWedRows[0]['name'])
               else:
                    # return message saying nobody available mon
                    db.execute("UPDATE output SET wednesday = ? WHERE rowId = ?", 'UNFILLED', x)

               availableThurRows = db.execute("SELECT name FROM staffers WHERE thursday = 1 AND thBool = 0 ORDER BY shifts ASC")
               preferNotThurRows = db.execute("SELECT name FROM staffers WHERE thursday = 2 AND thBool = 0 ORDER BY shifts ASC")
               if len(availableThurRows) > 0:
                    # update the output table with the name of the available person
                    db.execute("UPDATE output SET thursday = ? WHERE rowId = ?", availableThurRows[0]['name'], x)
                    # update the person's shift count
                    countRow = db.execute("SELECT shifts FROM staffers WHERE name = ?", availableThurRows[0]['name'])
                    count = countRow[0]['shifts']
                    db.execute("UPDATE staffers SET shifts = ?, thBool = 1 WHERE name = ?", count + 1, availableThurRows[0]['name'])
               elif len(preferNotThurRows) > 0:
                    # select prefer-not-tos
                    db.execute("UPDATE output SET thursday = ? WHERE rowId = ?", preferNotThurRows[0]['name'], x)
                     # update the person's shift count
                    countRow = db.execute("SELECT shifts FROM staffers WHERE name = ?", preferNotThurRows[0]['name'])
                    count = countRow[0]['shifts']
                    db.execute("UPDATE staffers SET shifts = ?, thBool = 1 WHERE name = ?", count + 1, preferNotThurRows[0]['name'])
               else:
                    # return message saying nobody available mon
                    db.execute("UPDATE output SET thursday = ? WHERE rowId = ?", 'UNFILLED', x)

               availableFriRows = db.execute("SELECT name FROM staffers WHERE friday = 1 AND frBool = 0 ORDER BY shifts ASC")
               preferNotFriRows = db.execute("SELECT name FROM staffers WHERE friday = 2 AND frBool = 0 ORDER BY shifts ASC")
               if len(availableFriRows) > 0:
                    # update the output table with the name of the available person
                    db.execute("UPDATE output SET friday = ? WHERE rowId = ?", availableFriRows[0]['name'], x)
                    # update the person's shift count
                    countRow = db.execute("SELECT shifts FROM staffers WHERE name = ?", availableFriRows[0]['name'])
                    count = countRow[0]['shifts']
                    db.execute("UPDATE staffers SET shifts = ?, frBool = 1 WHERE name = ?", count + 1, availableFriRows[0]['name'])
               elif len(preferNotFriRows) > 0:
                    # select prefer-not-tos
                    db.execute("UPDATE output SET friday = ? WHERE rowId = ?", preferNotFriRows[0]['name'], x)
                     # update the person's shift count
                    countRow = db.execute("SELECT shifts FROM staffers WHERE name = ?", preferNotFriRows[0]['name'])
                    count = countRow[0]['shifts']
                    db.execute("UPDATE staffers SET shifts = ?, frBool = 1 WHERE name = ?", count + 1, preferNotFriRows[0]['name'])
               else:
                    # return message saying nobody available mon
                    db.execute("UPDATE output SET friday = ? WHERE rowId = ?", 'UNFILLED', x)

               availableSatRows = db.execute("SELECT name FROM staffers WHERE saturday = 1 AND saBool = 0 ORDER BY shifts ASC")
               preferNotSatRows = db.execute("SELECT name FROM staffers WHERE saturday = 2 AND saBool = 0 ORDER BY shifts ASC")
               if len(availableSatRows) > 0:
                    # update the output table with the name of the available person
                    db.execute("UPDATE output SET saturday = ? WHERE rowId = ?", availableSatRows[0]['name'], x)
                    # update the person's shift count
                    countRow = db.execute("SELECT shifts FROM staffers WHERE name = ?", availableSatRows[0]['name'])
                    count = countRow[0]['shifts']
                    db.execute("UPDATE staffers SET shifts = ?, saBool = 1 WHERE name = ?", count + 1, availableSatRows[0]['name'])
               elif len(preferNotSatRows) > 0:
                    # select prefer-not-tos
                    db.execute("UPDATE output SET saturday = ? WHERE rowId = ?", preferNotSatRows[0]['name'], x)
                     # update the person's shift count
                    countRow = db.execute("SELECT shifts FROM staffers WHERE name = ?", preferNotSatRows[0]['name'])
                    count = countRow[0]['shifts']
                    db.execute("UPDATE staffers SET shifts = ?, saBool = 1 WHERE name = ?", count + 1, preferNotSatRows[0]['name'])
               else:
                    # return message saying nobody available mon
                    db.execute("UPDATE output SET saturday = ? WHERE rowId = ?", 'UNFILLED', x)

               availableSunRows = db.execute("SELECT name FROM staffers WHERE sunday = 1 AND suBool = 0 ORDER BY shifts ASC")
               preferNotSunRows = db.execute("SELECT name FROM staffers WHERE sunday = 2 AND suBool = 0 ORDER BY shifts ASC")
               if len(availableSunRows) > 0:
                    # update the output table with the name of the available person
                    db.execute("UPDATE output SET sunday = ? WHERE rowId = ?", availableSunRows[0]['name'], x)
                    # update the person's shift count
                    countRow = db.execute("SELECT shifts FROM staffers WHERE name = ?", availableSunRows[0]['name'])
                    count = countRow[0]['shifts']
                    db.execute("UPDATE staffers SET shifts = ?, suBool = 1 WHERE name = ?", count + 1, availableSunRows[0]['name'])
               elif len(preferNotSunRows) > 0:
                    # select prefer-not-tos
                    db.execute("UPDATE output SET sunday = ? WHERE rowId = ?", preferNotSunRows[0]['name'], x)
                     # update the person's shift count
                    countRow = db.execute("SELECT shifts FROM staffers WHERE name = ?", preferNotSunRows[0]['name'])
                    count = countRow[0]['shifts']
                    db.execute("UPDATE staffers SET shifts = ?, suBool = 1 WHERE name = ?", count + 1, preferNotSunRows[0]['name'])
               else:
                    # return message saying nobody available mon
                    db.execute("UPDATE output SET sunday = ? WHERE rowId = ?", 'UNFILLED', x)

          outputRows = db.execute("SELECT * FROM output")
          return render_template("output.html", outputRows=outputRows)
     else:

          return render_template("output.html", outputRows=outputRows)
