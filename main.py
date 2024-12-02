from flask import Flask
from flask_restx import Api
from routes.chercheur import api as chercheur_api
from routes.faculte import api as faculte_api
from routes.laboratoire import api as laboratoire_api
from routes.publication import api as publication_api

app = Flask(__name__)

# Swagger setup
api = Api(
    app,
    title="Research Management System API",
    version="1.0",
    description="A comprehensive API for managing researchers, faculties, laboratories, and publications.",
    doc="/"  # Swagger UI path
)

# Register namespaces
api.add_namespace(chercheur_api, path="/chercheur")
api.add_namespace(faculte_api, path="/faculte")
api.add_namespace(laboratoire_api, path="/laboratoire")
api.add_namespace(publication_api, path="/publication")

if __name__ == '__main__':
    app.run(debug=True)
