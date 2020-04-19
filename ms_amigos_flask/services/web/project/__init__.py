import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import and_


app = Flask(__name__)
app.config.from_object("project.config.Config")
db = SQLAlchemy(app)


# Defines the movies class and all their methods


class Amigo (db.Model):
    __tablename__ = 'amigos'
    # relotion amigos attributes
    id = db.Column(db.Integer, primary_key=True)
    amigo1 = db.Column(db.Integer)
    amigo2 = db.Column(db.Integer)

    # Methohd to create a amigos relation.
    # id is not required and not suggested, used for tests.
    def __init__(self, amigo1, amigo2):
        self.amigo1 = amigo1
        self.amigo2 = amigo2


    # method to insert a movie to the database
    def insert(self):
        db.session.add(self)
        db.session.commit()

    # Method to patch a movie
    def update(self):
        db.session.commit()

    # Method to delete a movie
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format1(self):
        return {
            'amigo1': self.amigo1
        }
    def format2(self):
        return {
            'amigo2': self.amigo2
        }    


    # GET Methods
    # returns a success message and a list of desired class.
    # Can take a page argument for pagination, 1  by default.



    @app.route('/amigos/<idlista>',methods=['GET'])
    def get_amigos(idlista):

        lista1= Amigo.query.distinct(Amigo.amigo2).filter(Amigo.amigo1==idlista)
        lista2= Amigo.query.distinct(Amigo.amigo1).filter(Amigo.amigo2 == idlista).all()
        current1 = [element.format2() for element in lista1]
        current2 = [element.format1() for element in lista2]
        return jsonify({
            'success': True,
            'amigos2da': current1,
            'amigos1ra': current2
        })


    # DELETE Methods
    # takes an id and returns a success message and the element id

    @app.route('/amigos/<amigo1_id>/<amigo2_id>', methods=['DELETE'])
    def delete_movie(amigo1_id,amigo2_id):

        amigo = Amigo.query.filter(and_(Amigo.amigo1 == amigo1_id,Amigo.amigo2 == amigo2_id)).one_or_none()
        if amigo is None:
            amigo = Amigo.query.filter(and_(Amigo.amigo2 == amigo1_id, Amigo.amigo1 == amigo2_id)).one_or_none()
        
        if amigo is None:
            abort(404)
        try:
            amigo.delete()
            return jsonify({
                'success': True,
                'deleted': amigo1_id,
                'deleted2': amigo2_id
            })
        except:
            abort(422)
  

    # POST Methods
    # return a succes message and the information about de new element

    @app.route('/amigos', methods=['POST'])
    def add_amigo():
        body = request.get_json()
        amigo1 = body.get('amigo1', None)
        amigo2 = body.get('amigo2', None)

        flag = Amigo.query.filter(and_(Amigo.amigo1 == amigo1, Amigo.amigo2 == amigo2)).one_or_none()
        flag2 = Amigo.query.filter(and_(Amigo.amigo2 == amigo1, Amigo.amigo1 == amigo2)).one_or_none()

        if flag is None and flag2 is None:

            try:
                newAmistad = Amigo(amigo1=amigo1, amigo2=amigo2)
                newAmistad.insert()
                return jsonify({
                    'success': True,
                })
            except:
                abort(422)
        else:        
         return 'relacion existente'


    @app.route('/')
    def main_page():
        return "please use one of the implemented endpoints"

    # Error handlers
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404


    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(500)
    def server_error():
        return jsonify({
            "success": False,
            "error": 500,
            "message": "server error"
        }), 500
