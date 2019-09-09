import pandas as pd

from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import create_engine
#  import sqlalchemy
import psycopg2
# from sqlalchemy import create_engine

engine = create_engine('postgresql://postgres:Peter@1947@localhost/VotingProject')
    
# import os
# import pandas as pd
# import numpy as np
# import sqlalchemy
# from sqlalchemy.ext.automap import automap_base
# from sqlalchemy.orm import Session
# from sqlalchemy import create_engine

# from flask import Flask, jsonify, render_template
# from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


#################################################
# Database Setup
#################################################

# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db/bellybutton.sqlite"
# db = SQLAlchemy(app)

# # reflect an existing database into a new model
# Base = automap_base()
# # reflect the tables
# Base.prepare(db.engine, reflect=True)

# # Save references to each table
# Samples_Metadata = Base.classes.sample_metadata
# Samples = Base.classes.samples


@app.route("/")
def index():
    """Return the homepage."""
    return render_template("index.html")


@app.route("/names")
def names():
    """Return a list of sample names."""
    regionList = ["All", "Appalachian","Heartland","Mid-Atlantic",
            "Midwest","Mountain","New England","Pacific",
               "Southeast","Southwest","Other"];
    return jsonify(regionList);


@app.route("/samples/<sample>")
def samples(sample):
    # """Return `otu_ids`, `otu_labels`,and `sample_values`."""
    
    region = sample
    # region = "Pacific"
    print("region: " + region)

    combined_df = pd.read_sql("combined_by_county",engine)
    print(combined_df.head())
    if region != "All":
        combined_df = combined_df.loc[combined_df["region"] == region,:]
    print(combined_df.head())
    data_df = combined_df[["nonwhite_pct","rep2016","dem2016"]]
    bins = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    group_names = ["0-10", "10-20", "20-30", "30-40", "40-50",
               "50-60", "60-70", "70-80", "80-90", "90-100"]
    data_df["ind"] = pd.cut(data_df["nonwhite_pct"], bins, labels=group_names)
    data_df["bin"] = pd.cut(data_df["nonwhite_pct"], bins, labels=group_names)
    by_bin = data_df.groupby(["ind"])
    rep_tot = by_bin["rep2016"].sum()
    dem_tot = by_bin["dem2016"].sum()
    summary = pd.DataFrame({"Rep":rep_tot, "Dem": dem_tot})
    binList = group_names
    repValues = list(summary["Rep"])
    demValues = list(summary["Dem"])
    data = {
        "bins": binList,
        "rep_values": repValues,
        "dem_values": demValues 
    }
    print(data)
    return jsonify(data)


if __name__ == "__main__":
    app.run()
