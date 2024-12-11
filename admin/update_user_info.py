
from flask import json, jsonify
import db

def update_user_info(data):
    connection = db.connect_to_mysql()
    if not connection:
        return json.dumps({"error": "Failed to connect to the database."}), 500
    
    try:
        with connection.cursor() as cursor:
            update_table_user(cursor,data)
            connection.commit()

            update_table_submission_record_national_id(cursor,data)
            connection.commit()
            
            output = {
                "message": "User information updated successfully.",
                "updated_info": data  
            }
    except Exception as e:
        return json.dumps({"error": f"An error occurred while fetching user data: {e}"}), 500
    
    finally:
        connection.close()

    return output

def update_table_user(cursor,data):
            sql = """
            UPDATE user
            SET 
                name = %s,
                surname = %s,
                job_position = %s,
                is_patient = %s,
                is_osm = %s,
                is_specialist = %s,
                is_admin = %s,
                email = %s,
                province = %s,
                national_id = %s,
                hospital = %s,
                phone = %s,
                license = %s
                WHERE id = %s;
            """
            cursor.execute(sql, (
                data['name'], 
                data['surname'], 
                data['job_position'], 
                data['is_patient'], 
                data['is_osm'], 
                data['is_specialist'], 
                data['is_admin'], 
                data['email'], 
                data['province'], 
                data['national_id'], 
                data['hospital'], 
                data['phone'],
                data['license'], 
                data['id'],
            ))

def update_table_submission_record_national_id(cursor,data):
            sql = """
            UPDATE submission_record
            SET 
                patient_national_id = %s
                WHERE patient_id = %s;
            """
            cursor.execute(sql, (data['national_id'],data['id'],))