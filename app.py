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
app.config['ALLOWED_FILE_EXTENSIONS'] = ['XLSX','XLS']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

db = SQLAlchemy(app)

class Player_Name(db.Model):
    __tablename__ = "player_Name"

    id = db.Column(db.Integer, primary_key = True)
    player_name = db.Column(db.String, index = True)
    game_playes = db.relationship('Player', backref = 'games', lazy = 'dynamic') #to Plyer tabel
    average_player = db.relationship('Player_Average', backref = 'games', lazy = 'dynamic') #to Player_Average tabel


class Player_Average(db.Model):
    __tablename__ = "player_Average"

    id = db.Column(db.Integer, primary_key = True)
    player_average_id = db.Column(db.Integer,db.ForeignKey('player_Name.id'))
    players_name = db.Column(db.String, index = True)
    Opponent = db.Column(db.String, index = True)
    Position = db.Column(db.String, nullable=True, index = True)
    Goals = db.Column(db.Float, nullable=True, index = True)
    Assists = db.Column(db.Float, nullable=True, index = True)
    Chances = db.Column(db.Float, nullable=True, index = True)
    Chances_successful = db.Column(db.Float, nullable=True, index = True)
    Chances_present_of_conversion = db.Column(db.Float, nullable=True, index = True)
    Сhances_created = db.Column(db.Float, nullable=True, index = True)
    Fouls = db.Column(db.Float, nullable=True, index = True)
    Fouls_suffered = db.Column(db.Float, nullable=True, index = True)
    Yellow_cards = db.Column(db.Float, nullable=True, index = True)
    Red_cards = db.Column(db.Float, nullable=True, index = True)
    Offsides = db.Column(db.Float, nullable=True, index = True)
    Shots = db.Column(db.Float, nullable=True, index = True)
    Shots_on_target = db.Column(db.Float, nullable=True, index = True)
    Expected_goals = db.Column(db.Float, nullable=True, index = True)
    Passes = db.Column(db.Float, nullable=True, index = True)
    Accurate_passes_present = db.Column(db.Float, nullable=True, index = True)
    Unnamed_fuckin_22W = db.Column(db.Float, nullable=True, index = True)
    Unnamed_fuckin_23X = db.Column(db.Float, nullable=True, index = True)
    Key_passes = db.Column(db.Float, nullable=True, index = True)
    Key_passes_accuracy_present = db.Column(db.Float, nullable=True, index = True)
    Crosses = db.Column(db.Float, nullable=True, index = True)
    Accurate_crosses_present = db.Column(db.Float, nullable=True, index = True)
    Lost_balls = db.Column(db.Float, nullable=True, index = True)
    Lost_balls_in_own_half = db.Column(db.Float, nullable=True, index = True)
    Ball_recoveries = db.Column(db.Float, nullable=True, index = True)
    Ball_recoveries_in_opponents_half = db.Column(db.Float, nullable=True, index = True)
    Challenges = db.Column(db.Float, nullable=True, index = True)
    Challenges_won_present = db.Column(db.Float, nullable=True, index = True)
    Defensive_challenges = db.Column(db.Float, nullable=True, index = True)
    Challenges_in_defence_won_present = db.Column(db.Float, nullable=True, index = True)
    Attacking_challenges = db.Column(db.Float, nullable=True, index = True)
    Challenges_in_attack__won_present = db.Column(db.Float, nullable=True, index = True)
    Air_challenges = db.Column(db.Float, nullable=True, index = True)
    Air_challenges_won = db.Column(db.Float, nullable=True, index = True)
    Air_challenges_won_present = db.Column(db.Float, nullable=True, index = True)
    Dribbles = db.Column(db.Float, nullable=True, index = True)
    Successful_dribbles_present = db.Column(db.Float, nullable=True, index = True)
    Tackles = db.Column(db.Float, nullable=True, index = True)
    Tackles_won_present = db.Column(db.Float, nullable=True, index = True)
    Ball_interceptions = db.Column(db.Float, nullable=True, index = True)
    Free_ball_pick_ups = db.Column(db.Float, nullable=True, index = True)
    Challenges_won = db.Column(db.Float, nullable=True, index = True)
    Defensive_challenges_won = db.Column(db.Float, nullable=True, index = True)
    Attacking_challenges_won = db.Column(db.Float, nullable=True, index = True)
    # Air_challenges_won_Percent = db.Column(db.Float, nullable=True, index = True)
    Dribbles_successful = db.Column(db.Float, nullable=True, index = True)
    Tackles_successful = db.Column(db.Float, nullable=True, index = True)
    Accurate_passes = db.Column(db.Float, nullable=True, index = True)
    Key_passes = db.Column(db.Float, nullable=True, index = True)
    Key_passes_accurate = db.Column(db.Float, nullable=True, index = True)
    Crosses_accurate = db.Column(db.Float, nullable=True, index = True)
    Successful_actions_Percent = db.Column(db.Float, nullable=True, index = True)
    Shots_on_target_Percent = db.Column(db.Float, nullable=True, index = True)
    Shots_on_post_bar = db.Column(db.Float, nullable=True, index = True)
    Opponents_xG_with_a_player_on = db.Column(db.Float, nullable=True, index = True)
    Net_xG_xG_player_on_opp_teams_xG = db.Column(db.Float, nullable=True, index = True)
    Defensive_xG_xG_of_shots_made_by_guarded_player = db.Column(db.Float, nullable=True, index = True)
    Minutes_played = db.Column(db.Float, nullable=True, index = True)
    Total_actions = db.Column(db.Float, nullable=True, index = True)
    Successful_actions = db.Column(db.Float, nullable=True, index = True)
    Shots_wide = db.Column(db.Float, nullable=True, index = True)
    Blocked_shots = db.Column(db.Float, nullable=True, index = True)
    Expected_assists = db.Column(db.Float, nullable=True, index = True)
    xG_per_shot = db.Column(db.Float, nullable=True, index = True)
    xG_per_goal = db.Column(db.Float, nullable=True, index = True)
    xG_conversion = db.Column(db.Float, nullable=True, index = True)
    xG_with_a_player_on = db.Column(db.Float, nullable=True, index = True)
    Defensive_xG_per_shot = db.Column(db.Float, nullable=True, index = True)
    Unnamed_fuckin_4E = db.Column(db.Float, nullable=True, index = True)
    Unnamed_fuckin_16Q = db.Column(db.Float, nullable=True, index = True)
    Unnamed_fuckin_17R = db.Column(db.Float, nullable=True, index = True)


class Player(db.Model):
    __tablename__ = "players_data"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    player_id = db.Column(db.Integer, db.ForeignKey('player_Name.id')) #colum to plyer_name
    players_name = db.Column(db.String, index = True)
    Opponent = db.Column(db.String, index = True)
    Position = db.Column(db.String, nullable=True, index = True)
    Goals = db.Column(db.Float, nullable=True, index = True)
    Assists = db.Column(db.Float, nullable=True, index = True)
    Chances = db.Column(db.Float, nullable=True, index = True)
    Chances_successful = db.Column(db.Float, nullable=True, index = True)
    Chances_present_of_conversion = db.Column(db.Float, nullable=True, index = True)
    Сhances_created = db.Column(db.Float, nullable=True, index = True)
    Fouls = db.Column(db.Float, nullable=True, index = True)
    Fouls_suffered = db.Column(db.Float, nullable=True, index = True)
    Yellow_cards = db.Column(db.Float, nullable=True, index = True)
    Red_cards = db.Column(db.Float, nullable=True, index = True)
    Offsides = db.Column(db.Float, nullable=True, index = True)
    Shots = db.Column(db.Float, nullable=True, index = True)
    Shots_on_target = db.Column(db.Float, nullable=True, index = True)
    Expected_goals = db.Column(db.Float, nullable=True, index = True)
    Passes = db.Column(db.Float, nullable=True, index = True)
    Accurate_passes_present = db.Column(db.Float, nullable=True, index = True)
    Unnamed_fuckin_22W = db.Column(db.Float, nullable=True, index = True)
    Unnamed_fuckin_23X = db.Column(db.Float, nullable=True, index = True)
    Key_passes = db.Column(db.Float, nullable=True, index = True)
    Key_passes_accuracy_present = db.Column(db.Float, nullable=True, index = True)
    Crosses = db.Column(db.Float, nullable=True, index = True)
    Accurate_crosses_present = db.Column(db.Float, nullable=True, index = True)
    Lost_balls = db.Column(db.Float, nullable=True, index = True)
    Lost_balls_in_own_half = db.Column(db.Float, nullable=True, index = True)
    Ball_recoveries = db.Column(db.Float, nullable=True, index = True)
    Ball_recoveries_in_opponents_half = db.Column(db.Float, nullable=True, index = True)
    Challenges = db.Column(db.Float, nullable=True, index = True)
    Challenges_won_present = db.Column(db.Float, nullable=True, index = True)
    Defensive_challenges = db.Column(db.Float, nullable=True, index = True)
    Challenges_in_defence_won_present = db.Column(db.Float, nullable=True, index = True)
    Attacking_challenges = db.Column(db.Float, nullable=True, index = True)
    Challenges_in_attack__won_present = db.Column(db.Float, nullable=True, index = True)
    Air_challenges = db.Column(db.Float, nullable=True, index = True)
    Air_challenges_won = db.Column(db.Float, nullable=True, index = True)
    Air_challenges_won_present = db.Column(db.Float, nullable=True, index = True)
    Dribbles = db.Column(db.Float, nullable=True, index = True)
    Successful_dribbles_present = db.Column(db.Float, nullable=True, index = True)
    Tackles = db.Column(db.Float, nullable=True, index = True)
    Tackles_won_present = db.Column(db.Float, nullable=True, index = True)
    Ball_interceptions = db.Column(db.Float, nullable=True, index = True)
    Free_ball_pick_ups = db.Column(db.Float, nullable=True, index = True)
    Challenges_won = db.Column(db.Float, nullable=True, index = True)
    Defensive_challenges_won = db.Column(db.Float, nullable=True, index = True)
    Attacking_challenges_won = db.Column(db.Float, nullable=True, index = True)
    # Air_challenges_won_Percent = db.Column(db.Float, nullable=True, index = True)
    Dribbles_successful = db.Column(db.Float, nullable=True, index = True)
    Tackles_successful = db.Column(db.Float, nullable=True, index = True)
    Accurate_passes = db.Column(db.Float, nullable=True, index = True)
    Key_passes = db.Column(db.Float, nullable=True, index = True)
    Key_passes_accurate = db.Column(db.Float, nullable=True, index = True)
    Crosses_accurate = db.Column(db.Float, nullable=True, index = True)
    Successful_actions_Percent = db.Column(db.Float, nullable=True, index = True)
    Shots_on_target_Percent = db.Column(db.Float, nullable=True, index = True)
    Shots_on_post_bar = db.Column(db.Float, nullable=True, index = True)
    Opponents_xG_with_a_player_on = db.Column(db.Float, nullable=True, index = True)
    Net_xG_xG_player_on_opp_teams_xG = db.Column(db.Float, nullable=True, index = True)
    Defensive_xG_xG_of_shots_made_by_guarded_player = db.Column(db.Float, nullable=True, index = True)
    Minutes_played = db.Column(db.Float, nullable=True, index = True)
    Total_actions = db.Column(db.Float, nullable=True, index = True)
    Successful_actions = db.Column(db.Float, nullable=True, index = True)
    Shots_wide = db.Column(db.Float, nullable=True, index = True)
    Blocked_shots = db.Column(db.Float, nullable=True, index = True)
    Expected_assists = db.Column(db.Float, nullable=True, index = True)
    xG_per_shot = db.Column(db.Float, nullable=True, index = True)
    xG_per_goal = db.Column(db.Float, nullable=True, index = True)
    xG_conversion = db.Column(db.Float, nullable=True, index = True)
    xG_with_a_player_on = db.Column(db.Float, nullable=True, index = True)
    Defensive_xG_per_shot = db.Column(db.Float, nullable=True, index = True) 
    Unnamed_fuckin_4E = db.Column(db.Float, nullable=True, index = True)
    Unnamed_fuckin_16Q = db.Column(db.Float, nullable=True, index = True)
    Unnamed_fuckin_17R = db.Column(db.Float, nullable=True, index = True)

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
        if request.form['submit_button'] == 'Upload to player_Name tabel': #upload to player_Name tabel
            ecxel_file = request.files['ecxel']
            if not allowed_file(ecxel_file.filename):
                print('file is not xlsx')
                return redirect(request.url)
            else:
                new_df = pd.read_excel(ecxel_file)
                new_df = new_df.fillna(0)

                ext = ecxel_file.filename.rsplit('.')[0]
                ext2 = ext.rsplit('_')[-1:]
                player_name_1= ' '.join(ext2)

                all_names = Player_Name.query.all()
                existing_players= []
                for name in all_names:
                    existing_players.append(name.player_name)
                # print(existing_players)

                if player_name_1 in existing_players:
                    print('this player exist')
                    return redirect(request.url)
                
                first_playername = Player_Name(player_name= player_name_1)
                db.session.add(first_playername)
                db.session.commit()
                # player_name_id = Player_Name.query.all()
                dataframe_1 = pd.read_sql('''SELECT * FROM "player_Name" ORDER BY id DESC LIMIT 1''', con = db.engine)
                # print(dataframe_1)
                player_id_number = dataframe_1.loc[0][0]
                # print(player_id_number)

                # cleaning the file
                to_drop = ['Date', 'Unnamed: 1','score','InStat Index']
                new_df.drop(columns=to_drop, inplace=True)
                new_df.insert(0,'players name', player_name_1, True)
                new_df.insert(0,'player_id', player_id_number, True)

                #for firest version- new_df.rename(columns={'players name':'players_name','Chances successful':'Chances_successful', "Chances, % of conversion":'Chances_present_of_conversion', 'Сhances created':'Сhances_created', 'Fouls suffered':'Fouls_suffered', 'Yellow cards':'Yellow_cards', 'Red cards':'Red_cards', 'Shots on target':'Shots_on_target','xG (Expected goals)':'Expected_goals', 'Accurate passes, %':'Accurate_passes_present', 'Key passes':'Key_passes', 'Key passes accuracy, %':'Key_passes_accuracy_present', 'Accurate crosses, %':'Accurate_crosses_present', 'Lost balls':'Lost_balls', "Lost balls in own half":"Lost_balls_in_own_half", 'Ball recoveries':'Ball_recoveries', "Ball recoveries in opponent's half":'Ball_recoveries_in_opponents_half', 'Challenges won, %':'Challenges_won_present', 'Defensive challenges':'Defensive_challenges', 'Challenges in defence won, %':'Challenges_in_defence_won_present', 'Attacking challenges':'Attacking_challenges', 'Challenges in attack / won, %':'Challenges_in_attack__won_present', 'Air challenges':'Air_challenges', 'Air challenges won, %':'Air_challenges_won_present', 'Successful dribbles, %':'Successful_dribbles_present', 'Tackles won, %':'Tackles_won_present', 'Ball interceptions':'Ball_interceptions', 'Free ball pick ups':'Free_ball_pick_ups'}, inplace=True)
                new_df.rename(columns={'players name':'players_name','Chances successful':'Chances_successful', "Chances, % of conversion":'Chances_present_of_conversion', 'Сhances created':'Сhances_created', 'Fouls suffered':'Fouls_suffered', 'Yellow cards':'Yellow_cards', 'Red cards':'Red_cards', 'Shots on target':'Shots_on_target','xG (Expected goals)':'Expected_goals', 'Accurate passes, %':'Accurate_passes_present',"Unnamed: 4":'Unnamed_fuckin_4E',"Unnamed: 16":'Unnamed_fuckin_16Q',"Unnamed: 17":'Unnamed_fuckin_17R',"Unnamed: 22":'Unnamed_fuckin_22W',"Unnamed: 23":'Unnamed_fuckin_23X', 'Key passes':'Key_passes', 'Key passes accuracy, %':'Key_passes_accuracy_present', 'Accurate crosses, %':'Accurate_crosses_present', 'Lost balls':'Lost_balls', "Lost balls in own half":"Lost_balls_in_own_half", 'Ball recoveries':'Ball_recoveries', "Ball recoveries in opponent's half":'Ball_recoveries_in_opponents_half', 'Challenges won, %':'Challenges_won_present', 'Defensive challenges':'Defensive_challenges', 'Challenges in defence won, %':'Challenges_in_defence_won_present', 'Attacking challenges':'Attacking_challenges', 'Challenges in attack / won, %':'Challenges_in_attack__won_present', 'Air challenges':'Air_challenges','Air challenges won':'Air_challenges_won', "Air challenges won, %":'Air_challenges_won_present', 'Successful dribbles, %':'Successful_dribbles_present', 'Tackles won, %':'Tackles_won_present', 'Ball interceptions':'Ball_interceptions', 'Free ball pick ups':'Free_ball_pick_ups','Challenges won':'Challenges_won','Defensive challenges won':'Defensive_challenges_won','Attacking challanges won':'Attacking_challenges_won','Attacking challenges won':'Attacking_challenges_won','Dribbles successful':'Dribbles_successful','Tackles successful':'Tackles_successful','Accurate passes':'Accurate_passes','Key passes':'Key_passes','Key passes accurate':'Key_passes_accurate','Crosses accurate':'Crosses_accurate','Successful actions, %':'Successful_actions_Percent','Shots on target, %':'Shots_on_target_Percent','Shots on post / bar':'Shots_on_post_bar',"Opponent's xG with a player on":"Opponents_xG_with_a_player_on","Net xG (xG player on - opp. team's xG)":"Net_xG_xG_player_on_opp_teams_xG","Defensive xG (xG of shots made by guarded player)":"Defensive_xG_xG_of_shots_made_by_guarded_player",'Minutes played':'Minutes_played','Total actions':'Total_actions','Successful actions':'Successful_actions','Shots wide':'Shots_wide','Blocked shots':'Blocked_shots','Expected assists':'Expected_assists','xG per shot':'xG_per_shot','xG per goal':'xG_per_goal','xG conversion':'xG_conversion',"xG with a player on":'xG_with_a_player_on','Defensive xG per shot':'Defensive_xG_per_shot'}, inplace=True)
                def delete(item):
                    if item == "-":
                        item = 0
                        return item
                    elif '%' in str(item):
                        return item[:item.find('%')]
                    else:
                        return item
                new_df = new_df.applymap(delete)
                shape = new_df.shape[0] -1


                df_average = new_df[new_df["Opponent"] == "Average per match"]
                
                found = new_df[new_df['Opponent'].str.contains('Average per match')]
                if len(found) == 0:
                    print( "F U C K YYYYYYYYY")
                    df_average = new_df[new_df["Opponent"] == "Total"]
                
                to_drop = ['player_id']
                df_average.drop(columns=to_drop, inplace=True)
                df_average.rename(columns={'player_id':'player_average_id'})
                df_average.insert(0,'player_average_id', player_id_number, True)
            
                df_average.to_sql(name='player_Average', con=db.engine, if_exists='append',  index=False)
                db.session.commit()

                new_df = new_df.drop([shape])
                new_df.to_sql(name='players_data', con=db.engine, if_exists='append',  index=False)
                db.session.commit()

                all_data = Player.query.all()
                tabel=new_df.to_html()
                dataframe = pd.read_sql('''SELECT * FROM "player_Average"''', con = db.engine)
                dataframe = dataframe.to_html()

            # return render_template('index.html',all_data=all_data , tabel=tabel, dataframe=dataframe)
            return redirect(request.url)

        
        elif request.form['submit_button'] == 'show_parameters':
            parameters_1 = request.form["parameters_1"]
            parameters_2 = request.form["parameters_2"]
            player_1 = request.form["player_1"]
            player_2 = request.form["player_2"]
            player_3 = request.form["player_3"]

            dataframe = pd.read_sql('''SELECT * FROM "player_Average"''', con = db.engine)
            player_Name_options_list = dataframe['players_name'].tolist()
            tabel_parameters = dataframe.columns.values.tolist()


            tabel_of_firest_parameter = dataframe[(dataframe['players_name']==player_1) | (dataframe['players_name']==player_2)| (dataframe['players_name']==player_3)]
            tabel_of_firest_parameter = tabel_of_firest_parameter[["players_name", parameters_1, parameters_2]]
            tabel_of_firest_parameter = tabel_of_firest_parameter.fillna(0)
            tabel_of_firest_parameter['ratio_A/B'] = tabel_of_firest_parameter[parameters_1]/tabel_of_firest_parameter[parameters_2]
            # print(tabel_of_firest_parameter)
            # tabel_of_firest_parameter = tabel_of_firest_parameter.replace("inf",0)
            # print(tabel_of_firest_parameter)
            dan_1=tabel_of_firest_parameter.columns.values.tolist()
            dan_2=tabel_of_firest_parameter.iloc[0].tolist()
            dan_3=tabel_of_firest_parameter.iloc[1].tolist()
            dan_4=tabel_of_firest_parameter.iloc[2].tolist()
            tabel_of_firest_parameter = tabel_of_firest_parameter.to_html()


            return render_template('index.html',dataframe=tabel_of_firest_parameter, tabel_parameters=tabel_parameters,player_Name_options_list=player_Name_options_list,dan_1=dan_1,dan_2=dan_2,dan_3=dan_3,dan_4=dan_4)
            # return redirect(request.url)

    dataframe = pd.read_sql('''SELECT * FROM "player_Average"''', con = db.engine)
    player_Name_options_list = dataframe['players_name'].tolist()
    tabel_parameters = dataframe.columns.values.tolist()
    # dataframe = dataframe.to_html()

    tabel_of_firest_parameter = dataframe[(dataframe['players_name']=="Tzlil Nechemia") | (dataframe['players_name']=="Idan Ahadnani") | (dataframe['players_name']=="Ran Israel Vaturi")]
    tabel_of_firest_parameter = tabel_of_firest_parameter[["players_name", 'Challenges', 'Challenges_in_defence_won_present']]
    tabel_of_firest_parameter['ratio_A/B'] = tabel_of_firest_parameter['Challenges_in_defence_won_present']/tabel_of_firest_parameter['Challenges']
    dan_1=tabel_of_firest_parameter.columns.values.tolist()
    dan_2=tabel_of_firest_parameter.iloc[0].tolist()
    dan_3=tabel_of_firest_parameter.iloc[1].tolist()
    dan_4=tabel_of_firest_parameter.iloc[2].tolist()
    dataframe = tabel_of_firest_parameter.to_html()

    return render_template('index.html',dataframe=dataframe, tabel_parameters=tabel_parameters,player_Name_options_list=player_Name_options_list, dan_1=dan_1,dan_2=dan_2,dan_3=dan_3,dan_4=dan_4)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        if request.form['submit_button'] == 'export':
                    dataframe = pd.read_sql('''SELECT * FROM "player_Average"''', con = db.engine)
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

    return render_template("upload.html")

@app.route('/parameters5', methods=['GET', 'POST'])
def parameters():

    if request.method == 'POST':
        if request.form['submit_button'] == 'show_5parameters':
            parameters_1 = request.form["parameters_1"]
            print(parameters_1)
            parameters_2 = request.form["parameters_2"]
            parameters_3 = request.form["parameters_3"]
            parameters_4 = request.form["parameters_4"]
            parameters_5 = request.form["parameters_5"]
            player_1 = request.form["player_1"]
            player_2 = request.form["player_2"]
            player_3 = request.form["player_3"]
            player_4 = request.form["player_4"]
            player_5 = request.form["player_5"]

            dataframe = pd.read_sql('''SELECT * FROM "player_Average"''', con = db.engine)
            player_Name_options_list = dataframe['players_name'].tolist()
            tabel_parameters = dataframe.columns.values.tolist()

            tabel_of_firest_parameter = dataframe[(dataframe['players_name']==player_1) | (dataframe['players_name']==player_2)| (dataframe['players_name']==player_3)| (dataframe['players_name']==player_4)| (dataframe['players_name']==player_5)]
            tabel_of_firest_parameter = tabel_of_firest_parameter[["players_name", parameters_1, parameters_2, parameters_3, parameters_4, parameters_5]]
            tabel_of_firest_parameter = tabel_of_firest_parameter.fillna(0)
            # print(tabel_of_firest_parameter)
            dan_1=tabel_of_firest_parameter.columns.values.tolist()
            dan_2=tabel_of_firest_parameter.iloc[0].tolist()
            dan_3=tabel_of_firest_parameter.iloc[1].tolist()
            dan_4=tabel_of_firest_parameter.iloc[2].tolist()
            dan_5=tabel_of_firest_parameter.iloc[3].tolist()
            dan_6=tabel_of_firest_parameter.iloc[4].tolist()

            tabel_of_firest_parameter = tabel_of_firest_parameter.to_html()


            return render_template('parameters5.html',dataframe=tabel_of_firest_parameter, tabel_parameters=tabel_parameters,player_Name_options_list=player_Name_options_list,dan_1=dan_1,dan_2=dan_2,dan_3=dan_3,dan_4=dan_4,dan_5=dan_5,dan_6=dan_6)
            # return redirect(request.url)

    dataframe = pd.read_sql('''SELECT * FROM "player_Average"''', con = db.engine)
    player_Name_options_list = dataframe['players_name'].tolist()
    tabel_parameters = dataframe.columns.values.tolist()
    # dataframe = dataframe.to_html()

    tabel_of_firest_parameter = dataframe[(dataframe['players_name']=="Tzlil Nechemia") | (dataframe['players_name']=="Idan Ahadnani") | (dataframe['players_name']=="Ran Israel Vaturi") | (dataframe['players_name']=="Dan Bitton") | (dataframe['players_name']=="Nadav Aviv Niddam")]
    tabel_of_firest_parameter = tabel_of_firest_parameter[["players_name", "Passes", "Attacking_challenges", "Dribbles", "Accurate_passes_present", "Key_passes_accuracy_present"]]
    tabel_of_firest_parameter = tabel_of_firest_parameter.fillna(0)
    dan_1=tabel_of_firest_parameter.columns.values.tolist()
    dan_2=tabel_of_firest_parameter.iloc[0].tolist()
    dan_3=tabel_of_firest_parameter.iloc[1].tolist()
    dan_4=tabel_of_firest_parameter.iloc[2].tolist()
    dan_5=tabel_of_firest_parameter.iloc[3].tolist()
    dan_6=tabel_of_firest_parameter.iloc[4].tolist()
    dataframe = tabel_of_firest_parameter.to_html()

    return render_template("parameters5.html",dataframe=dataframe, tabel_parameters=tabel_parameters,player_Name_options_list=player_Name_options_list,dan_1=dan_1,dan_2=dan_2,dan_3=dan_3,dan_4=dan_4,dan_5=dan_5,dan_6=dan_6)


@app.route('/scatter', methods=['GET', 'POST'])
def scatterpage():

    if request.method == 'POST':
        if request.form['submit_button'] == 'show_scatter':
            parameters_1 = request.form["parameters_1"]
            parameters_2 = request.form["parameters_2"]
            player_1 = request.form["player_1"]
            player_2 = request.form["player_2"]
            player_3 = request.form["player_3"]
            player_4 = request.form["player_4"]
            player_5 = request.form["player_5"]
            player_6 = request.form["player_6"]
            player_7 = request.form["player_7"]
            player_8 = request.form["player_8"]
            player_9 = request.form["player_9"]
            player_10 = request.form["player_10"]
            player_11 = request.form["player_11"]
            player_12 = request.form["player_12"]
            player_13 = request.form["player_13"]
            player_14 = request.form["player_14"]
            player_15 = request.form["player_15"]
            player_16 = request.form["player_16"]
            player_17 = request.form["player_17"]
            player_18 = request.form["player_18"]
            player_19 = request.form["player_19"]
            player_20 = request.form["player_20"]

            dataframe = pd.read_sql('''SELECT * FROM "player_Average"''', con = db.engine)
            player_Name_options_list = dataframe['players_name'].tolist()
            tabel_parameters = dataframe.columns.values.tolist()

            tabel_of_firest_parameter = dataframe[(dataframe['players_name']==player_1) | (dataframe['players_name']==player_2)| (dataframe['players_name']==player_3)| (dataframe['players_name']==player_4)| (dataframe['players_name']==player_5)| (dataframe['players_name']==player_6)| (dataframe['players_name']==player_7)| (dataframe['players_name']==player_8)|(dataframe['players_name']==player_9) | (dataframe['players_name']==player_10)| (dataframe['players_name']==player_11)| (dataframe['players_name']==player_12)| (dataframe['players_name']==player_13)| (dataframe['players_name']==player_14)| (dataframe['players_name']==player_15)| (dataframe['players_name']==player_16)| (dataframe['players_name']==player_17)| (dataframe['players_name']==player_18)| (dataframe['players_name']==player_19)| (dataframe['players_name']==player_20)]
            tabel_of_firest_parameter = tabel_of_firest_parameter[["players_name", parameters_1, parameters_2]]
            tabel_of_firest_parameter = tabel_of_firest_parameter.fillna(0)
            tabel_of_firest_parameter = tabel_of_firest_parameter [[parameters_1 ,parameters_2,"players_name"]]
            # print(tabel_of_firest_parameter)
            dan_1=tabel_of_firest_parameter.columns.values.tolist()
            dan_2=tabel_of_firest_parameter.iloc[0].tolist()
            dan_3=tabel_of_firest_parameter.iloc[1].tolist()
            dan_4=tabel_of_firest_parameter.iloc[2].tolist()
            dan_5=tabel_of_firest_parameter.iloc[3].tolist()
            dan_6=tabel_of_firest_parameter.iloc[4].tolist()
            dan_7=tabel_of_firest_parameter.iloc[5].tolist()
            dan_8=tabel_of_firest_parameter.iloc[6].tolist()
            dan_9=tabel_of_firest_parameter.iloc[7].tolist()
            dan_10=tabel_of_firest_parameter.iloc[8].tolist()
            dan_11=tabel_of_firest_parameter.iloc[9].tolist()
            dan_12=tabel_of_firest_parameter.iloc[10].tolist()
            dan_13=tabel_of_firest_parameter.iloc[11].tolist()
            dan_14=tabel_of_firest_parameter.iloc[12].tolist()
            dan_15=tabel_of_firest_parameter.iloc[13].tolist()
            dan_16=tabel_of_firest_parameter.iloc[14].tolist()
            dan_17=tabel_of_firest_parameter.iloc[15].tolist()
            dan_18=tabel_of_firest_parameter.iloc[16].tolist()
            dan_19=tabel_of_firest_parameter.iloc[17].tolist()
            dan_20=tabel_of_firest_parameter.iloc[18].tolist()
            dan_21=tabel_of_firest_parameter.iloc[19].tolist()

            tabel_of_firest_parameter = tabel_of_firest_parameter.to_html()


            return render_template('scatter.html',dataframe=tabel_of_firest_parameter, tabel_parameters=tabel_parameters,player_Name_options_list=player_Name_options_list, dan_2=dan_2, dan_3=dan_3, dan_4=dan_4, dan_5=dan_5, dan_6=dan_6, dan_7=dan_7, dan_8=dan_8, dan_9=dan_9, dan_10=dan_10, dan_11=dan_11, dan_12=dan_12, dan_13=dan_13, dan_14=dan_14, dan_15=dan_15, dan_16=dan_16, dan_17=dan_17, dan_18=dan_18, dan_19=dan_19, dan_20=dan_20, dan_21=dan_21)
            
    
    dataframe = pd.read_sql('''SELECT * FROM "player_Average"''', con = db.engine)
    player_Name_options_list = dataframe['players_name'].tolist()
    tabel_parameters = dataframe.columns.values.tolist()
    dataframe = dataframe.to_html() 

    return render_template("scatter.html",dataframe=dataframe, tabel_parameters=tabel_parameters,player_Name_options_list=player_Name_options_list)

@app.route('/testing', methods=['GET', 'POST'])
def testing():
    return render_template("testing.html")
