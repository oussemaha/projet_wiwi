from flask import request, jsonify
from flask_restx import Namespace, Resource, fields
from db import get_db_connection

api = Namespace("Laboratoire", description="Operations related to laboratoires")

# Swagger model for Laboratoire
laboratoire_model = api.model('Laboratoire', {
    'labno': fields.Integer(required=True, description="Laboratory number (Primary Key)"),
    'labnom': fields.String(required=True, description="Laboratory name"),
    'facno': fields.Integer(required=True, description="Associated faculty number"),
})

@api.route('/')
class LaboratoireList(Resource):
    @api.doc('list_laboratoires')
    def get(self):
        """List all laboratoires"""
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM LABORATOIRE")
        laboratoires = cursor.fetchall()
        cursor.close()
        connection.close()
        return jsonify([list(laboratoire) for laboratoire in laboratoires])

    @api.doc('create_laboratoire')
    @api.expect(laboratoire_model)
    def post(self):
        """Create a new laboratoire"""
        data = request.json
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO LABORATOIRE (labno, labnom, facno)
            VALUES (%s, %s, %s)
        """, (data['labno'], data['labnom'], data['facno']))
        connection.commit()
        cursor.close()
        connection.close()
        return {"message": "Laboratoire created successfully"}, 201

@api.route('/<int:labno>')
@api.param('labno', 'The laboratory ID')
class Laboratoire(Resource):
    @api.doc('get_laboratoire')
    def get(self, labno):
        """Fetch a laboratoire by ID"""
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM LABORATOIRE WHERE labno = %s", (labno,))
        laboratoire = cursor.fetchone()
        cursor.close()
        connection.close()
        if laboratoire:
            return list(laboratoire)
        api.abort(404, "Laboratoire not found")

    @api.doc('update_laboratoire')
    @api.expect(laboratoire_model)
    def put(self, labno):
        """Update a laboratoire"""
        data = request.json
        connection = get_db_connection()
        cursor = connection.cursor()

        updates = []
        params = []
        for key, value in data.items():
            updates.append(f"{key} = %s")
            params.append(value)
        params.append(labno)

        if updates:
            cursor.execute(f"UPDATE LABORATOIRE SET {', '.join(updates)} WHERE labno = %s", tuple(params))
            connection.commit()

        cursor.close()
        connection.close()
        return {"message": "Laboratoire updated successfully"}

    @api.doc('delete_laboratoire')
    def delete(self, labno):
        """Delete a laboratoire by ID"""
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM LABORATOIRE WHERE labno = %s", (labno,))
        connection.commit()
        cursor.close()
        connection.close()
        return {"message": "Laboratoire deleted successfully"}, 204

@api.route('/faculte/<int:facno>/laboratoires')
@api.param('facno', 'The ID of the faculty')
class LaboratoireByFaculte(Resource):
    @api.doc('get_laboratoires_by_faculte')
    def get(self, facno):
        """Fetch a list of laboratoires for a given faculty ID"""
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM LABORATOIRE WHERE facno = %s", (facno,))
        laboratoires = cursor.fetchall()
        cursor.close()
        connection.close()

        if not laboratoires:
            api.abort(404, "No laboratoires found for this faculty ID")

        return jsonify([list(laboratoire) for laboratoire in laboratoires])
