from flask import Flask, request
import requests

from database import db_session, init_db
from models import Project, PackageRelease
from sqlalchemy import exc

app = Flask(__name__)

@app.route("/api/projects", methods=["POST"])
def add_project():
    # TODO
    # - Processar os pacotes recebidos
    # - Persistir informações no banco

    try:
        new_project = Project(name=request.json['name'])    # Salvando informação na tabela de Projects
        db_session.add(new_project)
        db_session.commit()

        packages = []
        err = 0

        for el in request.json['packages']:
            verify = requests.get('https://pypi.org/pypi/'+el['name']+'/json')   # Fazendo requisição para validar pacote

            if ('name' in el and 'version' in el and verify.status_code == 200):    # Package com nome e versão, que foi verificado via PyPI
                if (el['version'] in verify.json()['releases']): 
                    project_packs = PackageRelease(
                        name=el['name'],
                        version=el['version'],
                        project_id=new_project.id
                    )
                    db_session.add(project_packs)
                    db_session.commit()
                    packages.append({ 'name': el['name'], "version": el['version'] })
                else: 
                    err =+ 1

            elif ('name' in el and verify.status_code == 200):   # Package com nome, mas sem versão, que tem versão atribuida via resposta do PyPI
                project_packs = PackageRelease(
                    name=el['name'],
                    version=verify.json()['info']['version'],
                    project_id=new_project.id
                )
                db_session.add(project_packs)
                db_session.commit()
                packages.append({ 'name': el['name'], "version": verify.json()['info']['version'] })
            
            elif (verify.status_code == 404):   # Verifica se o package não foi encontrado
                err =+ 1

        if (err == 0):
            return {
                "name": new_project.name,
                "packages": packages
            }, 201
        else:
            return { "error": "One or more packages doesn't exist" }, 400

    except exc.IntegrityError:
        return { "error": "This project already exists! Try another!" }, 400

    except:
        return { "error": "An error was occurred. Try again later!" }, 500


@app.route("/api/projects/<string:project_name>", methods=["GET"])
def show_project_detail(project_name):
    # TODO
    # - Retornar informações do projeto
    
    try:
        project = Project.query.filter_by(name=project_name).first()
        packages = []

        for el in project.package_releases:
            packages.append({ 'name': el.name, "version": el.version })
        
        return { 
            "name": project.name, 
            "packages": packages 
        }
        
    except AttributeError:
        return { "error": "This project no exists! Try another!" }, 404
    
    except:
        return { "error": "An error was occurred. Try again later!" }, 500


@app.errorhandler(404)
def page_not_found(error):
    return {"error": "This page does not exist"}, 404


@app.route("/api/projects/<string:project_name>", methods=["DELETE"])
def delete_project(project_name):
    # TODO
    # - Apagar o projeto indicado
    return {'foo': 'bar'}


@app.teardown_appcontext
def shutdown_session(exception=None):
    # Remover sessões ao final de cada request
    db_session.remove()
