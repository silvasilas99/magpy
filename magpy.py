from flask import Flask, request
import requests

from database import db_session, init_db
from models import Project, PackageRelease

app = Flask(__name__)

@app.route("/api/projects", methods=["POST"])
def add_project():
    # TODO
    # - Processar os pacotes recebidos
    # - Persistir informações no banco

    new_project = Project(name=request.json['name'])    # Salvando informação na tabela de Projects
    db_session.add(new_project)
    db_session.commit()

    packages = []
    for el in request.json['packages']:
        project_packs = PackageRelease(
            name=el['name'],
            version=el['version'],
            project_id=new_project.id
        )
        db_session.add(project_packs)
        db_session.commit()
        packages.append({ 'name': el['name'], "version": el['version'] })

    return {
        "name": new_project.name,
        "packages": packages
    }


@app.route("/api/projects/<string:project_name>", methods=["GET"])
def show_project_detail(project_name):
    # TODO
    # - Retornar informações do projeto
    project = Project.query.filter_by(name=project_name).first()
    packages = []

    for el in project.package_releases:
        packages.append({ 'name': el.name, "version": el.version })
    
    return { 
        "name": project.name, 
        "packages": packages 
    }


@app.route("/api/projects/<string:project_name>", methods=["DELETE"])
def delete_project(project_name):
    # TODO
    # - Apagar o projeto indicado
    return {'foo': 'bar'}


@app.teardown_appcontext
def shutdown_session(exception=None):
    # Remover sessões ao final de cada request
    db_session.remove()
