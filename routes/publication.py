from flask_restx import Namespace, Resource, fields
from db import get_db_connection
from flask import request, jsonify

api = Namespace("Publication", description="Operations related to publications")

# Swagger model for Publication
publication_model = api.model('Publication', {
    'pubno': fields.String(required=True, description="Publication number (Primary Key)"),
    'titre': fields.String(required=True, description="Title of the publication"),
    'theme': fields.String(required=False, description="Theme of the publication"),
    'type': fields.String(required=True, description="Type of the publication"),
    'volume': fields.Integer(required=False, description="Volume of the publication"),
    'date': fields.String(required=False, description="Date of publication"),
    'apparition': fields.String(required=False, description="Apparition details"),
    'editeur': fields.String(required=False, description="Editor details"),
})

@api.route('/')
class PublicationList(Resource):
    @api.doc('list_publications')
    def get(self):
        """List all publications"""
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM PUBLICATION")
        publications = cursor.fetchall()
        cursor.close()
        connection.close()
        return jsonify([list(publication) for publication in publications])

    @api.doc('create_publication')
    @api.expect(publication_model)
    def post(self):
        """Create a new publication"""
        data = request.json
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO PUBLICATION (pubno, titre, theme, type, volume, date, apparition, editeur)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            data['pubno'], data['titre'], data.get('theme'), data['type'],
            data.get('volume'), data.get('date'), data.get('apparition'),
            data.get('editeur')
        ))
        connection.commit()
        cursor.close()
        connection.close()
        return {"message": "Publication created successfully"}, 201
