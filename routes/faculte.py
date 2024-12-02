from flask import request, jsonify
from flask_restx import Namespace, Resource, fields
from db import get_db_connection

api = Namespace("Faculte", description="Operations related to facultes")

# Swagger model for Faculte
faculte_model = api.model('Faculte', {
    'facno': fields.Integer(required=True, description="Faculty number (Primary Key)"),
    'facnom': fields.String(required=True, description="Faculty name"),
    'adresse': fields.String(required=False, description="Faculty address"),
    'libelle': fields.String(required=False, description="Faculty description"),
})

@api.route('/')
class FaculteList(Resource):
    @api.doc('list_facultes')
    def get(self):
        """List all facultes"""
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM FACULTE")
        facultes = cursor.fetchall()
        cursor.close()
        connection.close()
        return jsonify([list(faculte) for faculte in facultes])

    @api.doc('create_faculte')
    @api.expect(faculte_model)
    def post(self):
        """Create a new faculte"""
        data = request.json
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO FACULTE (facno, facnom, adresse, libelle)
            VALUES (%s, %s, %s, %s)
        """, (data['facno'], data['facnom'], data.get('adresse'), data.get('libelle')))
        connection.commit()
        cursor.close()
        connection.close()
        return {"message": "Faculte created successfully"}, 201

@api.route('/<int:facno>')
@api.param('facno', 'The faculty ID')
class Faculte(Resource):
    @api.doc('get_faculte')
    def get(self, facno):
        """Fetch a faculte by ID"""
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM FACULTE WHERE facno = %s", (facno,))
        faculte = cursor.fetchone()
        cursor.close()
        connection.close()
        if faculte:
            return list(faculte)
        api.abort(404, "Faculte not found")

    @api.doc('update_faculte')
    @api.expect(faculte_model)
    def put(self, facno):
        """Update a faculte"""
        data = request.json
        connection = get_db_connection()
        cursor = connection.cursor()

        updates = []
        params = []
        for key, value in data.items():
            updates.append(f"{key} = %s")
            params.append(value)
        params.append(facno)

        if updates:
            cursor.execute(f"UPDATE FACULTE SET {', '.join(updates)} WHERE facno = %s", tuple(params))
            connection.commit()

        cursor.close()
        connection.close()
        return {"message": "Faculte updated successfully"}

    @api.doc('delete_faculte')
    def delete(self, facno):
        """Delete a faculte by ID"""
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM FACULTE WHERE facno = %s", (facno,))
        connection.commit()
        cursor.close()
        connection.close()
        return {"message": "Faculte deleted successfully"}, 204
