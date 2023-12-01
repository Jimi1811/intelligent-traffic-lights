import mysql.connector

class DatabaseDAO:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host="mysql-container",  # Actualizar con config del mysql
            user="root",
            password="root_password",
            database="mydb"
        )
        self.cursor = self.connection.cursor()

    def execute_query(self, query, params=None):
        self.cursor.execute(query, params)
        self.connection.commit()

    def fetch_data(self, query, params=None):
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def close_connection(self):
        self.connection.close()

class RecordingsDAO(DatabaseDAO):
    def __init__(self):
        super().__init__()

    def create_recording(self, recording_id, rpi_address, date):
        query = "INSERT INTO recordings (recording_id, rpi_address, date) VALUES (%s, %s, %s)"
        params = (recording_id, rpi_address, date)
        self.execute_query(query, params)

    def get_all_recordings(self):
        query = "SELECT * FROM recordings"
        return self.fetch_data(query)

    def get_recording_by_id(self, recording_id):
        query = "SELECT * FROM recordings WHERE recording_id = %s"
        params = (recording_id,)
        return self.fetch_data(query, params)

    def update_recording(self, recording_id, rpi_address, date):
        query = "UPDATE recordings SET rpi_address = %s, date = %s WHERE recording_id = %s"
        params = (rpi_address, date, recording_id)
        self.execute_query(query, params)

    def delete_recording(self, recording_id):
        query = "DELETE FROM recordings WHERE recording_id = %s"
        params = (recording_id,)
        self.execute_query(query, params)

class IntersectionsDAO(DatabaseDAO):
    def __init__(self):
        super().__init__()

    def create_intersection(self, intersection_id, avenue_status_1, avenue_status_2, number_vehicles, traffic_level, recording_id):
        query = "INSERT INTO intersections (intersection_id, avenue_status_1, avenue_status_2, number_vehicles, traffic_level, recording_id) VALUES (%s, %s, %s, %s, %s, %s)"
        params = (intersection_id, avenue_status_1, avenue_status_2, number_vehicles, traffic_level, recording_id)
        self.execute_query(query, params)

    def get_all_intersections(self):
        query = "SELECT * FROM intersections"
        return self.fetch_data(query)

    def get_intersection_by_id(self, intersection_id):
        query = "SELECT * FROM intersections WHERE intersection_id = %s"
        params = (intersection_id,)
        return self.fetch_data(query, params)

    def update_intersection(self, intersection_id, avenue_status_1, avenue_status_2, number_vehicles, traffic_level, recording_id):
        query = "UPDATE intersections SET avenue_status_1 = %s, avenue_status_2 = %s, number_vehicles = %s, traffic_level = %s, recording_id = %s WHERE intersection_id = %s"
        params = (avenue_status_1, avenue_status_2, number_vehicles, traffic_level, recording_id, intersection_id)
        self.execute_query(query, params)

    def delete_intersection(self, intersection_id):
        query = "DELETE FROM intersections WHERE intersection_id = %s"
        params = (intersection_id,)
        self.execute_query(query, params)
