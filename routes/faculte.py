from flask_restx import Namespace, Resource, fields
from db import get_db_connection
from flask import request, jsonify

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
