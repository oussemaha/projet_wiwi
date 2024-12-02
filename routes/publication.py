from flask import request, jsonify
from flask_restx import Namespace, Resource, fields
from db import get_db_connection

api = Namespace("Publication", description="Operations related to publications")

# Swagger model for Publication
publication_model = api.model('Publication', {
    'pubno': fields.String(required=True, description="Publication number (Primary Key)"),
    'titre': fields.String(required=True, description="Title of the publication"),
    'theme': fields.String(required=False, description="Theme of the publication"),
    'type': fields.String(required=True, description="Type of the publication (e.g., AS, PC)"),
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

@api.route('/<string:pubno>')
@api.param('pubno', 'The publication number')
class Publication(Resource):
    @api.doc('get_publication')
    def get(self, pubno):
        """Fetch a publication by ID"""
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM PUBLICATION WHERE pubno = %s", (pubno,))
        publication = cursor.fetchone()
        cursor.close()
        connection.close()
        if publication:
            return list(publication)
        api.abort(404, "Publication not found")

    @api.doc('update_publication')
    @api.expect(publication_model)
    def put(self, pubno):
        """Update a publication"""
        data = request.json
        connection = get_db_connection()
        cursor = connection.cursor()

        updates = []
        params = []
        for key, value in data.items():
            updates.append(f"{key} = %s")
            params.append(value)
        params.append(pubno)

        if updates:
            cursor.execute(f"UPDATE PUBLICATION SET {', '.join(updates)} WHERE pubno = %s", tuple(params))
            connection.commit()

        cursor.close()
        connection.close()
        return {"message": "Publication updated successfully"}

    @api.doc('delete_publication')
    def delete(self, pubno):
        """Delete a publication by ID"""
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM PUBLICATION WHERE pubno = %s", (pubno,))
        connection.commit()
        cursor.close()
        connection.close()
        return {"message": "Publication deleted successfully"}, 204

@api.route('/chercheur/<int:chno>/publications')
@api.param('chno', 'The ID of the researcher')
class PublicationsByChercheur(Resource):
    @api.doc('get_publications_by_chercheur')
    def get(self, chno):
        """Fetch a list of publications for a given researcher ID"""
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("""
            SELECT P.*
            FROM PUBLICATION P
            INNER JOIN PUBLIER PB ON P.pubno = PB.pubno
            WHERE PB.chno = %s
        """, (chno,))
        publications = cursor.fetchall()
        cursor.close()
        connection.close()

        if not publications:
            api.abort(404, "No publications found for this researcher ID")

        return jsonify([list(publication) for publication in publications])

