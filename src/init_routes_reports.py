from flask import render_template, request
from sqlalchemy import text

def init_routes_reports(app, db):

    @app.route("/reports/8")
    def report_8():
        locations = db.session.query(
            db.column('Name'),
            db.column('Address'),
            db.column('city'),
            db.column('Province'),
            db.column('PostalCode'),
            db.column('Phone'),
            db.column('WebAddress'),
            db.column('Type'),
            db.column('Capacity'),
            db.column('GeneralManagerName'),
            db.column('MinorClubMembersCount'),
            db.column('MajorClubMembersCount'),
            db.column('TeamCount')
        ).from_statement(text("""
            SELECT
                l.Name,
                l.Address,
                l.city,
                l.Province,
                l.PostalCode,
                l.Phone,
                l.WebAddress,
                l.Type,
                l.Capacity,
                CONCAT(p.FirstName, ' ', p.LastName) AS GeneralManagerName,
                SUM(CASE WHEN cm.Type = 'Minor' THEN 1 ELSE 0 END) AS MinorClubMembersCount,
                SUM(CASE WHEN cm.Type = 'Major' THEN 1 ELSE 0 END) AS MajorClubMembersCount,
                COUNT(DISTINCT t.TeamID) AS TeamCount
            FROM
                location AS l
                LEFT JOIN operatesat AS op ON op.LocationID = l.LocationID
                    AND (op.EndDate IS NULL OR op.EndDate < CURDATE())
                LEFT JOIN personnel AS p ON p.PersonnelID = op.PersonnelID
                    AND p.Role = 'Administrator'
                LEFT JOIN clubmemberlocation AS cml ON cml.LocationID = l.LocationID
                    AND (cml.EndDate IS NULL OR cml.EndDate < CURDATE())
                LEFT JOIN clubmember cm ON cm.ClubMemberID = cml.ClubMemberID
                LEFT JOIN team t ON t.LocationID = l.LocationID
            GROUP BY
                l.LocationID,
                l.Name,
                l.Address,
                l.city,
                l.Province,
                l.PostalCode,
                l.Phone,
                l.WebAddress,
                l.Type,
                l.Capacity,
                p.FirstName,
                p.LastName
            ORDER BY
                l.Province ASC,
                l.city ASC;
        """))

        return render_template('reports/8.html', data=locations)

    @app.route("/reports/9")
    def report_9():
        query = db.session.query(
            db.column('SecondaryFirstName'),
            db.column('SecondaryLastName'),
            db.column('SecondaryPhone'),
            db.column('ClubMemberID'),
            db.column('ClubMemberFirstName'),
            db.column('ClubMemberLastName'),
            db.column('DOB'),
            db.column('SSN'),
            db.column('MedicareCardNumber'),
            db.column('Phone'),
            db.column('Address'),
            db.column('City'),
            db.column('Province'),
            db.column('PostalCode'),
            db.column('Relationship')
        ).from_statement(text("""
            SELECT
                sfm.FirstName AS SecondaryFirstName,
                sfm.LastName AS SecondaryLastName,
                sfm.Phone AS SecondaryPhone,
                cm.ClubMemberID,
                cm.FirstName AS ClubMemberFirstName,
                cm.LastName AS ClubMemberLastName,
                cm.DOB,
                cm.SSN,
                cm.MedicareCardNumber,
                cm.Phone,
                cm.Address,
                cm.City,
                cm.Province,
                cm.PostalCode,
                ec.Relationship
            FROM
                secondaryfamilymember sfm
                JOIN emergencycontact ec ON sfm.SecondaryID = ec.SecondaryID
                JOIN clubmember cm ON ec.ClubMemberID = cm.ClubMemberID
            ORDER BY
                sfm.FirstName,
                sfm.LastName,
                cm.FirstName,
                cm.LastName;
        """))

        columns = query.column_descriptions
        keys = [col['name'] for col in columns]
        print(keys)

        return render_template('reports/genericTableTemplate.html', keys=keys, data=query, title="Family Member and Associated Club Members Report")

    @app.route("/reports/10")
    def report_10():
        location_id = request.args.get('location_id')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')

        query = db.session.query(
            db.column('HeadCoachFirstName'),
            db.column('HeadCoachLastName'),
            db.column('StartTime'),
            db.column('Address'),
            db.column('SessionType'),
            db.column('TeamName'),
            db.column('ScoreTeamA'),
            db.column('ScoreTeamB'),
            db.column('ClubMemberID'),
            db.column('PlayerFirstName'),
            db.column('PlayerLastName'),
            db.column('RoleInTeam')
        ).from_statement(text(f"""
            SELECT
                p.FirstName AS HeadCoachFirstName,
                p.LastName AS HeadCoachLastName,
                tf.StartTime,
                tf.Address,
                tf.SessionType,
                t.Name AS TeamName,
                tf.ScoreTeamA,
                tf.ScoreTeamB,
                pm.ClubMemberID,
                cm.FirstName AS PlayerFirstName,
                cm.LastName AS PlayerLastName,
                pm.RoleInTeam
            FROM
                teamformation tf
                JOIN formationteam ft ON tf.FormationID = ft.FormationID
                JOIN team t ON ft.TeamID = t.TeamID
                JOIN location l ON t.LocationID = l.LocationID
                LEFT JOIN teamcoach tc ON t.TeamID = tc.TeamID
                LEFT JOIN personnel p ON tc.PersonnelID = p.PersonnelID
                JOIN playsin pm ON tf.FormationID = pm.FormationID
                JOIN clubmember cm ON pm.ClubMemberID = cm.ClubMemberID
            WHERE
                l.LocationID = :location_id -- Replace with the desired location ID
                AND tf.Date BETWEEN :start_date AND :end_date -- Replace with the desired date range
            ORDER BY
                tf.date ASC,
                tf.StartTime ASC;
        """)).params(location_id=location_id, start_date=start_date, end_date=end_date)

        columns = query.column_descriptions
        keys = [col['name'] for col in columns]
        print(keys)

        return render_template('reports/genericTableTemplate.html', keys=keys, data=query, title="Active Club Members Assigned to All Volleyball Roles")

    @app.route("/reports/11")
    def report_11():
        
        clubmembers = db.session.query(
            db.column('ClubMemberID'),
            db.column('FirstName'),
            db.column('LastName')
        ).from_statement(text("""
            SELECT
                cm.ClubMemberID,
                cm.FirstName,
                cm.LastName
            FROM
                clubmember AS cm
                JOIN clubmemberlocation AS cml ON cm.ClubMemberID = cml.ClubMemberID
            WHERE
                cm.Status = 'Inactive'
                AND DATEDIFF(CURDATE(), cm.DateJoined) >= 730 -- 730 days = 2 years
            GROUP BY
                cm.ClubMemberID,
                cm.FirstName,
                cm.LastName
            HAVING
                COUNT(cml.LocationID) >= 2
            ORDER BY
                cm.ClubMemberID ASC;
        """))

        return render_template('reports/11.html', data=clubmembers)
    
    @app.route("/reports/12")
    def report_12():
        query = db.session.query(
            db.column('LocationName'),
            db.column('TotalTrainingSessions'),
            db.column('TotalPlayersInTrainingSessions'),
            db.column('TotalGameSessions'),
            db.column('TotalPlayersInGameSessions')
        ).from_statement(text("""
            SELECT
                l.Name AS LocationName,
                COUNT(DISTINCT CASE WHEN tf.SessionType = 'Training' THEN tf.FormationID END) AS TotalTrainingSessions,
                SUM(CASE WHEN tf.SessionType = 'Training' THEN PI.ClubMemberID ELSE 0 END) AS TotalPlayersInTrainingSessions,
                COUNT(DISTINCT CASE WHEN tf.SessionType = 'Game' THEN tf.FormationID END) AS TotalGameSessions,
                SUM(CASE WHEN tf.SessionType = 'Game' THEN PI.ClubMemberID ELSE 0 END) AS TotalPlayersInGameSessions
            FROM
                location l
                LEFT JOIN team t ON l.LocationID = t.LocationID
                LEFT JOIN formationteam ft ON t.TeamID = ft.TeamID
                LEFT JOIN teamformation tf ON ft.FormationID = ft.FormationID
                LEFT JOIN playsin PI ON tf.FormationID = PI.FormationID
            WHERE
                tf.Date BETWEEN '2025-01-01' AND '2025-05-31'
            GROUP BY
                l.Name
            HAVING
                COUNT(DISTINCT CASE WHEN tf.SessionType = 'Game' THEN tf.FormationID END) >= 4
            ORDER BY
                TotalGameSessions DESC;
        """))

        columns = query.column_descriptions
        keys = [col['name'] for col in columns]
        print(keys)

        return render_template('reports/genericTableTemplate.html', keys=keys, data=query, title="Location Team Session Summary (Training & Games)")

    @app.route("/reports/13")
    def report_13():
        
        clubmembers = db.session.query(
            db.column('ClubMemberID'),
            db.column('FirstName'),
            db.column('LastName'),
            db.column('Age'),
            db.column('Phone'),
            db.column('Email'),
            db.column('CurrentLocationNames')
        ).from_statement(text("""
            SELECT
                cm.ClubMemberID,
                cm.FirstName,
                cm.LastName,
                TIMESTAMPDIFF(YEAR, cm.DOB, CURDATE()) AS Age,
                cm.Phone,
                cm.Email,
                GROUP_CONCAT(
                    l.Name
                    ORDER BY
                        l.Name ASC SEPARATOR ', '
                ) AS CurrentLocationNames
            FROM
                clubmember cm
                LEFT JOIN playsin PI ON cm.ClubMemberID = PI.ClubMemberID
                LEFT JOIN clubmemberlocation cml ON cm.ClubMemberID = cml.ClubMemberID
                    AND cml.EndDate IS NULL
                LEFT JOIN location l ON cml.LocationID = l.LocationID
            WHERE
                cm.Status = 'Active'
                AND PI.FormationID IS NULL
            GROUP BY
                cm.ClubMemberID
            ORDER BY
                CurrentLocationNames,
                Age;
        """))

        return render_template('reports/13.html', data=clubmembers)
    
    @app.route("/reports/14")
    def report_14():
        
        clubmembers = db.session.query(
            db.column('ClubMemberID'),
            db.column('FirstName'),
            db.column('LastName'),
            db.column('DateJoined'),
            db.column('Age'),
            db.column('Phone'),
            db.column('Email'),
            db.column('CurrentLocationNames')
        ).from_statement(text("""
            SELECT
                cm.ClubMemberID,
                cm.FirstName,
                cm.LastName,
                cm.DateJoined,
                TIMESTAMPDIFF(YEAR, cm.DOB, cm.DateJoined) AS Age,
                cm.Phone,
                cm.Email,
                GROUP_CONCAT(
                    l.Name
                    ORDER BY
                        l.Name ASC SEPARATOR ', '
                ) AS CurrentLocationNames
            FROM
                clubmember cm
                LEFT JOIN clubmemberlocation cml ON cm.ClubMemberID = cml.ClubMemberID
                    AND (
                        cml.EndDate IS NULL
                        OR cml.EndDate < CURDATE()
                    )
                LEFT JOIN location l ON cml.LocationID = l.LocationID
            WHERE
                cm.Status LIKE "Active"
                AND TIMESTAMPDIFF(YEAR, cm.DOB, cm.DateJoined) < 18
                AND cm.`Type` LIKE "Major"
            GROUP BY
                cm.ClubMemberID
            ORDER BY
                CurrentLocationNames ASC,
                Age ASC;
        """))

        return render_template('reports/14.html', data=clubmembers)
    
    @app.route("/reports/15")
    def report_15():
        query = db.session.query(
            db.column('ClubMemberID'),
            db.column('FirstName'),
            db.column('LastName'),
            db.column('Age'),
            db.column('Phone'),
            db.column('Email'),
            db.column('CurrentLocationNames')
        ).from_statement(text("""
            SELECT
                cm.ClubMemberID,
                cm.FirstName,
                cm.LastName,
                TIMESTAMPDIFF(YEAR, cm.DOB, CURDATE()) AS Age,
                cm.Phone,
                cm.Email,
                GROUP_CONCAT(l.Name ORDER BY l.Name ASC SEPARATOR ', ') AS CurrentLocationNames
            FROM
                clubmember cm
                JOIN playsin PI ON cm.ClubMemberID = PI.ClubMemberID
                LEFT JOIN clubmemberlocation cml ON cm.ClubMemberID = cml.ClubMemberID
                    AND (cml.EndDate IS NULL OR cml.EndDate < CURDATE())
                LEFT JOIN location l ON cml.LocationID = l.LocationID
            WHERE
                cm.Status LIKE "Active"
            GROUP BY
                cm.ClubMemberID,
                cm.FirstName,
                cm.LastName,
                cm.DOB,
                cm.Phone,
                cm.Email
            HAVING
                COUNT(DISTINCT CASE WHEN PI.RoleInTeam = 'Setter' THEN 1 END) >= 1
                AND COUNT(DISTINCT CASE WHEN PI.RoleInTeam != 'Setter' THEN 1 END) = 0
            ORDER BY
                CurrentLocationNames ASC,
                cm.ClubMemberID ASC;
        """))

        columns = query.column_descriptions
        keys = [col['name'] for col in columns]
        print(keys)

        return render_template('reports/genericTableTemplate.html', keys=keys, data=query, title="Active Club Members Exclusively Assigned as Setters")

    @app.route("/reports/16")
    def report_16():
        query = db.session.query(
            db.column('ClubMemberID'),
            db.column('FirstName'),
            db.column('LastName'),
            db.column('Age'),
            db.column('Phone'),
            db.column('Email'),
            db.column('CurrentLocationNames')
        ).from_statement(text("""
            SELECT
                cm.ClubMemberID,
                cm.FirstName,
                cm.LastName,
                TIMESTAMPDIFF(YEAR, cm.DOB, CURDATE()) AS Age,
                cm.Phone,
                cm.Email,
                GROUP_CONCAT(l.Name ORDER BY l.Name ASC SEPARATOR ', ') AS CurrentLocationNames
            FROM
                clubmember cm
                LEFT JOIN playsin PI ON cm.ClubMemberID = PI.ClubMemberID
                LEFT JOIN clubmemberlocation cml ON cm.ClubMemberID = cml.ClubMemberID
                    AND (cml.EndDate IS NULL OR cml.EndDate < CURDATE())
                LEFT JOIN location l ON cml.LocationID = l.LocationID
            WHERE
                cm.Status LIKE "Active"
                AND PI.FormationID IS NOT NULL
            GROUP BY
                cm.ClubMemberID,
                cm.FirstName,
                cm.LastName,
                cm.DOB,
                cm.Phone,
                cm.Email
            HAVING
                COUNT(DISTINCT CASE WHEN PI.RoleInTeam = 'Setter' THEN 1 END) >= 1
                AND COUNT(DISTINCT CASE WHEN PI.RoleInTeam = 'Libero' THEN 1 END) >= 1
                AND COUNT(DISTINCT CASE WHEN PI.RoleInTeam = 'OutsideHitter' THEN 1 END) >= 1
                AND COUNT(DISTINCT CASE WHEN PI.RoleInTeam = 'OppositeHitter' THEN 1 END) >= 1
            ORDER BY
                CurrentLocationNames ASC,
                cm.ClubMemberID ASC;
        """))

        columns = query.column_descriptions
        keys = [col['name'] for col in columns]
        print(keys)

        return render_template('reports/genericTableTemplate.html', keys=keys, data=query, title="Active Club Members Assigned to All Volleyball Roles")

    @app.route("/reports/17")
    def report_17():
        query = db.session.query(
            db.column('FirstName'),
            db.column('LastName'),
            db.column('Phone')
        ).from_statement(text("""
            SELECT DISTINCT
                fm.FirstName,
                fm.LastName,
                fm.Phone
            FROM
                familymember fm
                JOIN isrelatedto ir ON fm.FamilySSN = ir.FamilySSN
                JOIN clubmember cm ON ir.ClubMemberID = cm.ClubMemberID
                JOIN personnel p ON fm.FamilySSN = p.SSN
                JOIN clubmemberlocation cml ON cm.ClubMemberID = cml.ClubMemberID
                    AND (cml.EndDate IS NULL OR cml.EndDate < CURDATE())
                JOIN operatesat op ON p.PersonnelID = op.PersonnelID
                    AND (op.EndDate IS NULL OR op.EndDate < CURDATE())
            WHERE
                cm.Status LIKE "Active"
                AND p.Role LIKE "HeadCoach"
                AND cml.LocationID = op.LocationID;
        """))

        columns = query.column_descriptions
        keys = [col['name'] for col in columns]
        print(keys)

        return render_template('reports/genericTableTemplate.html', keys=keys, data=query, title="Family Members Who Are Also Head Coaches at Given Location")

    @app.route("/reports/18")
    def report_18():
        query = db.session.query(
            db.column('ClubMemberID'),
            db.column('FirstName'),
            db.column('LastName'),
            db.column('Age'),
            db.column('Phone'),
            db.column('Email'),
            db.column('LocationName')
        ).from_statement(text("""
            SELECT
                c.ClubMemberID,
                c.FirstName,
                c.LastName,
                TIMESTAMPDIFF(YEAR, c.DOB, CURDATE()) AS Age,
                c.Phone,
                c.Email,
                l.Name AS LocationName
            FROM
                clubmember c
                JOIN playsin PI ON c.ClubMemberID = PI.ClubMemberID
                JOIN teamformation tf ON PI.FormationID = tf.FormationID
                JOIN formationteam ft ON tf.FormationID = ft.FormationID
                JOIN team t ON ft.TeamID = t.TeamID
                LEFT JOIN location l ON t.LocationID = l.LocationID
            WHERE
                c.Status = 'Active'
                AND (
                    (ft.Role = 'TeamA' AND tf.ScoreTeamA > tf.ScoreTeamB)
                    OR (ft.Role = 'TeamB' AND tf.ScoreTeamB > tf.ScoreTeamA)
                )
            ORDER BY
                l.Name ASC,
                c.ClubMemberID ASC;
        """))

        columns = query.column_descriptions
        keys = [col['name'] for col in columns]
        print(keys)

        return render_template('reports/genericTableTemplate.html', keys=keys, data=query, title="Undefeated Active Club Members (Never Lost a Game)")

    @app.route("/reports/19")
    def report_19():
        query = db.session.query(
            db.column('FirstName'),
            db.column('LastName'),
            db.column('NumberOfMinorMembers'),
            db.column('Phone'),
            db.column('Email'),
            db.column('CurrentLocationName'),
            db.column('Role')
        ).from_statement(text("""
            SELECT
                p.FirstName,
                p.LastName,
                COUNT(DISTINCT cm.ClubMemberID) AS NumberOfMinorMembers,
                p.Phone,
                p.Email,
                l.Name AS CurrentLocationName,
                p.Role
            FROM
                personnel p
                LEFT JOIN operatesat o ON p.PersonnelID = o.PersonnelID
                    AND (o.EndDate IS NULL OR o.EndDate < CURDATE())
                LEFT JOIN location l ON o.LocationID = l.LocationID
                JOIN isrelatedto ir ON p.SSN = ir.FamilySSN
                JOIN clubmember cm ON ir.ClubMemberID = cm.ClubMemberID
            WHERE
                p.Mandate LIKE "Volunteer"
                AND cm.Type LIKE "Minor"
            GROUP BY
                p.PersonnelID,
                p.FirstName,
                p.LastName,
                p.Phone,
                p.Email,
                l.Name,
                p.Role
            ORDER BY
                l.Name ASC,
                p.Role ASC,
                p.FirstName ASC,
                p.LastName ASC;
        """))

        columns = query.column_descriptions
        keys = [col['name'] for col in columns]
        print(keys)

        return render_template('reports/genericTableTemplate.html', keys=keys, data=query, title="Volunteers with Minor Family Members Report")