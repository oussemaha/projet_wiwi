from flask import request, jsonify
from flask_restx import Namespace, Resource, fields
from db import get_db_connection

# Define the namespace
api = Namespace("Chercheur", description="Operations related to chercheurs")

# Define the model for Swagger
chercheur_model = api.model('Chercheur', {
    'chno': fields.Integer(required=True, description="The unique identifier of the chercheur"),
    'chnom': fields.String(required=True, description="Name of the chercheur"),
    'grade': fields.String(required=True, description="Grade of the chercheur (e.g., PR, MC, etc.)"),
    'statut': fields.String(required=True, description="Statut of the chercheur (P or C)"),
    'daterecrut': fields.String(required=False, description="Recruitment date of the chercheur"),
    'salaire': fields.Float(required=False, description="Salary of the chercheur"),
    'prime': fields.Float(required=False, description="Prime or bonus for the chercheur"),
    'email': fields.String(required=True, description="Email of the chercheur"),
    'labno': fields.Integer(required=False, description="Laboratory number of the chercheur"),
    'facno': fields.Integer(required=False, description="Faculty number of the chercheur"),
})

@api.route('/')
class ChercheurList(Resource):
    @api.doc('list_chercheurs')
    def get(self):
        """List all chercheurs"""
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM CHERCHEUR")
        chercheurs = cursor.fetchall()
        cursor.close()
        connection.close()
        return jsonify([list(chercheur) for chercheur in chercheurs])

    @api.doc('create_chercheur')
    @api.expect(chercheur_model)
    def post(self):
        """Create a new chercheur"""
        data = request.json
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO CHERCHEUR (chno, chnom, grade, statut, daterecrut, salaire, prime, email, labno, facno)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            data['chno'], data['chnom'], data['grade'], data['statut'],
            data.get('daterecrut'), data.get('salaire'), data.get('prime'),
            data['email'], data.get('labno'), data.get('facno')
        ))
        connection.commit()
        cursor.close()
        connection.close()
        return {"message": "Chercheur created successfully"}, 201

@api.route('/<int:chno>')
@api.param('chno', 'The unique identifier of the chercheur')
class Chercheur(Resource):
    @api.doc('get_chercheur')
    def get(self, chno):
        """Fetch a chercheur by their ID"""
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM CHERCHEUR WHERE chno = %s", (chno,))
        chercheur = cursor.fetchone()
        cursor.close()
        connection.close()
        if chercheur:
            return list(chercheur)
        api.abort(404, "Chercheur not found")

    @api.doc('update_chercheur')
    @api.expect(chercheur_model)
    def put(self, chno):
        """Update an existing chercheur"""
        data = request.json
        connection = get_db_connection()
        cursor = connection.cursor()

        updates = []
        params = []
        for key, value in data.items():
            updates.append(f"{key} = %s")
            params.append(value)
        params.append(chno)

        if updates:
            cursor.execute(f"UPDATE CHERCHEUR SET {', '.join(updates)} WHERE chno = %s", tuple(params))
            connection.commit()

        cursor.close()
        connection.close()
        return {"message": "Chercheur updated successfully"}

    @api.doc('delete_chercheur')
    def delete(self, chno):
        """Delete a chercheur by their ID"""
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM CHERCHEUR WHERE chno = %s", (chno,))
        connection.commit()
        cursor.close()
        connection.close()
        return {"message": "Chercheur deleted successfully"}, 204

@api.route('/laboratoire/<int:labno>/chercheurs')
@api.param('labno', 'The ID of the laboratory')
class ChercheurByLaboratoire(Resource):
    @api.doc('get_chercheurs_by_laboratoire')
    def get(self, labno):
        """Fetch a list of chercheurs for a given laboratory ID"""
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM CHERCHEUR WHERE labno = %s", (labno,))
        chercheurs = cursor.fetchall()
        cursor.close()
        connection.close()

        if not chercheurs:
            api.abort(404, "No chercheurs found for this laboratory ID")

        return jsonify([list(chercheur) for chercheur in chercheurs])

