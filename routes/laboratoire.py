from flask_restx import Namespace, Resource, fields
from db import get_db_connection
from flask import request, jsonify

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
