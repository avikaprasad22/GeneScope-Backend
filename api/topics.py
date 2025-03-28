from flask import Blueprint, jsonify
from flask_restful import Api, Resource

topics_api = Blueprint('topics_api', __name__, url_prefix='/api')

# API docs https://flask-restful.readthedocs.io/en/latest/api.html
api = Api(topics_api)

class TopicAPI:
    @staticmethod
    def get_topics(name):
        topics = {
            "DNA Sequencing": {
                "name": "DNA Sequencing",
                "resource": "fivable",
            },
            "Genetic Mutation": {
                "name": "Genetic Mutation",
                "resource": "wikipedia",
            },              
        }
        return topics.get(name, {})  # Return empty dict if topic is not found

    class _DNA_Sequencing(Resource):
        def get(self):
            return jsonify(TopicAPI.get_topics("DNA Sequencing"))
        
    class _Genetic_Mutation(Resource):
        def get(self):
            return jsonify(TopicAPI.get_topics("Genetic Mutation"))
        
    class _Bulk(Resource):
        def get(self):
            # Correcting the function calls
            dna_sequencing_details = TopicAPI.get_topics("DNA Sequencing")
            genetic_mutation_details = TopicAPI.get_topics("Genetic Mutation")
            return jsonify({"topics": [dna_sequencing_details, genetic_mutation_details]})

    # Building REST API endpoints
    api.add_resource(_DNA_Sequencing, '/topics/dna_sequencing')
    api.add_resource(_Genetic_Mutation, '/topics/genetic_mutation')
    api.add_resource(_Bulk, '/topics')

# Register the endpoints
topics_api_instance = TopicAPI()
