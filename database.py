# import pandas as pd
# from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData


# # Connect to the database
# cur = create_engine('postgresql://postgres:1234@localhost:5432/test2')
# connection = cur.connect()
# # # Create the Games table with primary key
# # cur.execute("""
# #     CREATE TABLE Games (
# #         GAME_ID SERIAL PRIMARY KEY,
# #         MATCHUP VARCHAR(50),
# #         LOCATION VARCHAR(1),
# #         W VARCHAR(1),
# #         FINAL_MARGIN INTEGER
# #     );
# # """)

# # # Create the Players table with primary key
# # cur.execute("""
# #     CREATE TABLE Players (
# #         PLAYER_ID SERIAL PRIMARY KEY,
# #         PLAYER_NAME VARCHAR(50)
# #     );
# # """)

# # # Create the Defenders table with primary key
# # cur.execute("""
# #     CREATE TABLE Defenders (
# #         DEFENDER_ID SERIAL PRIMARY KEY,
# #         DEFENDER_NAME VARCHAR(50)
# #     );
# # """)

# # # Create the Shots table with primary and foreign keys
# # cur.execute("""
# #     CREATE TABLE Shots (
# #         SHOT_ID SERIAL PRIMARY KEY,
# #         GAME_ID INTEGER REFERENCES Games(GAME_ID),
# #         SHOT_NUMBER INTEGER,
# #         PERIOD INTEGER,
# #         GAME_CLOCK VARCHAR(8),
# #         SHOT_CLOCK FLOAT,
# #         DRIBBLES INTEGER,
# #         TOUCH_TIME FLOAT,
# #         SHOT_DIST FLOAT,
# #         PTS_TYPE INTEGER,
# #         SHOT_RESULT VARCHAR(7),
# #         CLOSE_DEF_DIST FLOAT,
# #         FGM INTEGER,
# #         PTS INTEGER
# #     );
# # """)

# # # Create the Shots_Defenders table with foreign keys
# # cur.execute("""
# #     CREATE TABLE Shots_Defenders (
# #         SHOT_ID INTEGER REFERENCES Shots(SHOT_ID),
# #         DEFENDER_ID INTEGER REFERENCES Defenders(DEFENDER_ID),
# #         CLOSEST_DEFENDER_PLAYER_ID INTEGER
# #     );
# # """)

# # # Load data from CSV file into a Pandas dataframe
# # df = pd.read_csv("shots_filtered.csv")

# # # Insert data into the Games table
# # for index, row in df.iterrows():
# #     cur.execute("""
# #         INSERT INTO Games (MATCHUP, LOCATION, W, FINAL_MARGIN)
# #         VALUES (%s, %s, %s, %s) RETURNING GAME_ID;
# #     """, (row["MATCHUP"], row["LOCATION"], row["W"], row["FINAL_MARGIN"]))
# #     game_id = cur.fetchone()[0]

# #     # Insert data into the Players table
# #     cur.execute("""
# #         INSERT INTO Players (PLAYER_NAME)
# #         VALUES (%s) RETURNING PLAYER_ID;
# #     """, (row["player_name"],))
# #     player_id = cur.fetchone()[0]

# #     # Insert data into the Defenders table
# #     cur.execute("""
# #         INSERT INTO Defenders (DEFENDER_NAME)
# #         VALUES (%s) RETURNING DEFENDER_ID;
# #     """, (row["CLOSEST_DEFENDER"],))
# #     defender_id = cur.fetchone()[0]

# #     # Insert data into the Shots table
# #     cur.execute("""
# #         INSERT INTO Shots (
# #             GAME_ID, SHOT_NUMBER, PERIOD, GAME_CLOCK, SHOT_CLOCK,
# #             DRIBBLES, TOUCH_TIME, SHOT_DIST, PTS_TYPE, SHOT_RESULT,
# #             CLOSE_DEF_DIST, FGM, PTS
# #         )
# #         VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING SHOT_ID;
# #     """, (
# #         game_id, row["SHOT_NUMBER"], row["PERIOD"], row["GAME_CLOCK"], row["SHOT_CLOCK"],
# #         row["DRIBBLES"], row["TOUCH_TIME"], row["SHOT_DIST"], row["PTS_TYPE"], row["SHOT_RESULT"],
# #         row["CLOSE_DEF_DIST"],


# # Insert data into the Games table


# df = pd.read_csv('shots_filtered.csv')


# for index, row in df.iterrows():
#     result = connection.execute("""
#         INSERT INTO Games (MATCHUP, LOCATION, W, FINAL_MARGIN)
#         VALUES (%s, %s, %s, %s);
#     """, (row["MATCHUP"], row["LOCATION"], row["W"], row["FINAL_MARGIN"]))
#     game_id = result.lastrowid

#     # Insert data into the Players table
#     result = connection.execute("""
#         INSERT INTO Players (PLAYER_NAME)
#         VALUES (%s);
#     """, (row["player_name"],))
#     player_id = result.lastrowid

#     # Insert data into the Defenders table
#     result = connection.execute("""
#         INSERT INTO Defenders (DEFENDER_NAME)
#         VALUES (%s);
#     """, (row["CLOSEST_DEFENDER"],))
#     defender_id = result.lastrowid

#     # Insert data into the Shots table
    
#     result = connection.execute("""
#         INSERT INTO Shots (
#             GAME_ID, SHOT_NUMBER, PERIOD, GAME_CLOCK, SHOT_CLOCK,
#             DRIBBLES, TOUCH_TIME, SHOT_DIST, PTS_TYPE, SHOT_RESULT,
#             CLOSE_DEF_DIST, FGM, PTS
#         )
#         VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
#     """, (
#         game_id, row["SHOT_NUMBER"], row["PERIOD"], row["GAME_CLOCK"], row["SHOT_CLOCK"],
#         row["DRIBBLES"], row["TOUCH_TIME"], row["SHOT_DIST"], row["PTS_TYPE"], row["SHOT_RESULT"],
#         row["CLOSE_DEF_DIST"], row["FGM"], row["PTS"]
#     ))
#     shot_id = result.lastrowid
    
#     # Insert data into the Shots_Defenders table
#     connection.execute("""
#         INSERT INTO Shots_Defenders (
#             SHOT_ID, DEFENDER_ID
#         )
#         VALUES (%s, %s);
#     """, (
#         shot_id, defender_id
#     ))

# # close the connection
# connection.close()