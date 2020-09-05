import os
from io import BytesIO
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, send_file
import pandas as pd
import numpy as np
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
import flask_excel as excel


app = Flask(__name__)
ENV = 'production'

if ENV == 'dev':
    app.denug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///myDB.db'
else:
    app.denug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://hjhsprtbfnahgt:4a3ac5df6d9e3db852691fcc734f659e740a896fa9ccd27e3ca9b0e1d80c5922@ec2-52-72-34-184.compute-1.amazonaws.com:5432/d4cs2h729n3io0'

app.config['FILE_UPLOAD']= 'C:/Users/Top/Documents/liad2/static/uploads'
app.config['ALLOWED_FILE_EXTENSIONS'] = ['XLSX']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

db = SQLAlchemy(app)

class Try_1(db.Model):
    __tablename__ = "Try_1"

    id = db.Column(db.Integer, primary_key = True)
    bbb = db.Column(db.Integer, index = True)
    ccc = db.Column(db.Integer, index = True)
    ddd = db.Column(db.Integer, index = True)
    eee = db.Column(db.Integer, index = True)

class Player(db.Model):
    __tablename__ = "all_players"

    players name = db.Column(db.String, index = True)
    Opponent = db.Column(db.String, index = True)
    Position = db.Column(db.String, nullable=True, index = True)
    Goals = db.Column(db.Integer, nullable=True, index = True)
    Assists = db.Column(db.Integer, nullable=True, index = True)
    Chances = db.Column(db.Integer, nullable=True, index = True)
    Chances_successful = db.Column(db.Integer, nullable=True, index = True)
    Chances,_% _of_conversion = db.Column(db.Integer, nullable=True, index = True)
    Сhances_created = db.Column(db.Integer, nullable=True, index = True)
    Fouls = db.Column(db.Integer, nullable=True, index = True)
    Fouls_suffered = db.Column(db.Integer, nullable=True, index = True)
    Yellow_cards = db.Column(db.Integer, nullable=True, index = True)
    Red_cards = db.Column(db.Integer, nullable=True, index = True)
    Offsides = db.Column(db.Integer, nullable=True, index = True)
    Shots = db.Column(db.Integer, nullable=True, index = True)
    Shots_on_target = db.Column(db.Integer, nullable=True, index = True)
    xG_(Expected_goals) = db.Column(db.Integer, nullable=True, index = True)
    Passes = db.Column(db.Integer, nullable=True, index = True)
    Accurate_passes,_% = db.Column(db.Integer, nullable=True, index = True)
    Key_passes = db.Column(db.Integer, nullable=True, index = True)
    Key_passes_accuracy,_% = db.Column(db.Integer, nullable=True, index = True)
    Crosses = db.Column(db.Integer, nullable=True, index = True)
    Accurate_crosses,_% = db.Column(db.Integer, nullable=True, index = True)
    Lost_balls = db.Column(db.Integer, nullable=True, index = True)
    Lost_balls_in_own_half = db.Column(db.Integer, nullable=True, index = True)
    Ball_recoveries = db.Column(db.Integer, nullable=True, index = True)
    Ball_recoveries_in_opponents_half = db.Column(db.Integer, nullable=True, index = True)
    Challenges = db.Column(db.Integer, nullable=True, index = True)
    Challenges_won,_% = db.Column(db.Integer, nullable=True, index = True)
    Defensive_challenges = db.Column(db.Integer, nullable=True, index = True)
    Challenges_in_defence_won,_% = db.Column(db.Integer, nullable=True, index = True)
    Attacking_challenges = db.Column(db.Integer, nullable=True, index = True)
    Challenges_in_attack_/_won,_% = db.Column(db.Integer, nullable=True, index = True)
    Air_challenges = db.Column(db.Integer, nullable=True, index = True)
    Air_challenges won,_% = db.Column(db.Integer, nullable=True, index = True)
    Dribbles = db.Column(db.Integer, nullable=True, index = True)
    Successful_dribbles,_% = db.Column(db.Integer, nullable=True, index = True)
    Tackles = db.Column(db.Integer, nullable=True, index = True)
    Tackles won,_% = db.Column(db.Integer, nullable=True, index = True)
    Ball_interceptions = db.Column(db.Integer, nullable=True, index = True)
    Free_ball_pick_ups = db.Column(db.Integer, nullable=True, index = True)


db.create_all()

def allowed_file(filename):
    if not "." in filename:
        return False
    ext = filename.rsplit('.',1)[1]
    if ext.upper() in app.config['ALLOWED_FILE_EXTENSIONS']:
        return True
    else:
        return False


@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if request.form['submit_button'] == 'Do Something':
            ecxel_file = request.files['ecxel']
            if not allowed_file(ecxel_file.filename):
                print('file is not xlsx')
                return redirect(request.url)
            else:
                filename = secure_filename(ecxel_file.filename)
                print(ecxel_file)
                # ecxel_file.save(os.path.join(app.config['FILE_UPLOAD'], filename))
                print('file saved')
                #printing the ecxel
                new_df = pd.read_excel(ecxel_file)
                print(new_df)
                # print(new_df.shape)
                # print(new_df.shape[0])
                for rew in range(new_df.shape[0]):
                    # print (new_df.iloc[rew])
                    x=6
                new_df.to_sql(name='Try_1', con=db.engine, if_exists='append',  index=False)
                db.session.commit()

                all_data = Try_1.query.all()
                print(all_data)
                tabel=new_df.to_html()

                dataframe = pd.read_sql('''SELECT * FROM "Try_1"''', con = db.engine)
                dataframe = dataframe.to_html()
                
            return render_template('index.html',all_data=all_data , tabel=tabel, dataframe=dataframe)
        elif request.form['submit_button'] == 'export':
                dataframe = pd.read_sql('''SELECT * FROM "Try_1"''', con = db.engine)
                #create an output stream
                output = BytesIO()
                writer = pd.ExcelWriter(output, engine='xlsxwriter')
                #taken from the original question
                dataframe.to_excel(writer, startrow = 0, merge_cells = False, sheet_name = "Sheet_1")                
                workbook = writer.book
                worksheet = writer.sheets["Sheet_1"]
                format = workbook.add_format()
                format.set_bg_color('#eeeeee')
                worksheet.set_column(0,9,28)
                #the writer has done its job
                writer.close()
                #go back to the beginning of the stream
                output.seek(0)
                #finally return the file
                return send_file(output, attachment_filename="testing.xlsx", as_attachment=True)

    dataframe = pd.read_sql('''SELECT * FROM "Try_1"''', con = db.engine)
    dataframe = dataframe.to_html()

    return render_template('index.html',dataframe=dataframe)

# @app.route("/export", methods=['GET'])
# def export_records():
#     return excel.make_response_from_array([[1, 2], [3, 4]], "csv",
#                                           file_name="export_data")

