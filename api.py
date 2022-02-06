from flask import Flask, request
from flask_restful import Resource, Api
import requests
app = Flask(__name__)
api = Api(app)

class Index(Resource):

    def get(self):

        return {'Atakan': 'Ciftci'}

class Temperature(Resource):

    def get(self):

        args = request.args
        city = args['city']

        response = requests.get(f"https://caseapi.bestcloudfor.me/temperature?city={city}")
        temperature = response.json()

        return temperature


api.add_resource(Index, '/')
api.add_resource(Temperature,'/temperature')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
