import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="simulation_db"
)

cursor = db.cursor()

# cursor.execute("CREATE DATABASE simulation_db")  - created a database

cursor.execute('''CREATE TABLE IF NOT EXISTS Credentials(
               username VARCHAR(50) PRIMARY KEY NOT NULL,
               password VARCHAR(64) NOT NULL,
               account_type CHAR(1) NOT NULL)''')
# using hash 256 bits

cursor.execute('''CREATE TABLE IF NOT EXISTS SavedProjects(
                projectID int PRIMARY KEY NOT NULL AUTO_INCREMENT,
                project_name VARCHAR(50) NOT NULL,
                userID VARCHAR(50) NOT NULL,
                FOREIGN KEY(userID) REFERENCES Credentials(username),
                FPS INT DEFAULT 60,
                date_created DATETIME)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS Objects(
                objectID INT AUTO_INCREMENT PRIMARY KEY,
                object_name VARCHAR(50) NOT NULL,
                projectID int NOT NULL,
                UNIQUE(object_name, projectID),
                FOREIGN KEY(projectID) REFERENCES SavedProjects(projectID),
                object_type VARCHAR(50) NOT NULL,
                position_x smallint UNSIGNED NOT NULL, position_y smallint UNSIGNED,
                velocity_x DECIMAL(10, 2), velocity_y DECIMAL(10, 2),
                force_x DECIMAL(10, 2), force_y DECIMAL(10, 2),
                angle DECIMAL(10, 2), mass DECIMAL(10, 2),
                friction DECIMAL(10, 2), elasticity DECIMAL(10, 2),
                radius DECIMAL(10, 2), width DECIMAL(10, 2), height DECIMAL(10, 2))''')

cursor.execute('''CREATE TABLE IF NOT EXISTS Questions(
                questionID int PRIMARY KEY NOT NULL AUTO_INCREMENT,
                model VARCHAR(50) NOT NULL,
                difficulty_level TEXT NOT NULL,
                question TEXT NOT NULL,
                correct_answer TEXT NOT NULL)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS ProgressTracker(
                questionID int NOT NULL,
                FOREIGN KEY(questionID) REFERENCES Questions(questionID),
                userID VARCHAR(50) NOT NULL,
                FOREIGN KEY(userID) REFERENCES Credentials(username),
                answer TEXT,
                result BOOLEAN,
                PRIMARY KEY (userID, questionID)
                )''')

db.commit()
