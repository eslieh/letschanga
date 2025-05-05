from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request, current_app
from models import db, Fundraiser
from flask_caching import Cache


# Parser for creating and updating
fundraiser_parser = reqparse.RequestParser()
fundraiser_parser.add_argument("title", type=str, required=True)
fundraiser_parser.add_argument("description", type=str, required=True)
fundraiser_parser.add_argument("goal_amount", type=float, required=True)
fundraiser_parser.add_argument("image_url", type=str)
fundraiser_parser.add_argument("deadline", type=str)  # Use YYYY-MM-DD

class FundraiserListResource(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        
        # Cache key for the list of fundraisers
        cache_key = f"user_fundraisers_{user_id}_page_{request.args.get('page', default=1, type=int)}_limit_{request.args.get('limit', default=10, type=int)}"
        cache = current_app.cache
        # Try to get cached response
        cached_data = cache.get(cache_key)
        if cached_data:
            return cached_data, 200  # Return cached response if it exists

        # Get pagination params
        page = request.args.get('page', default=1, type=int)
        limit = request.args.get('limit', default=10, type=int)

        fundraisers_query = Fundraiser.query.filter_by(user_id=user_id).order_by(Fundraiser.created_at.desc())
        pagination = fundraisers_query.paginate(page=page, per_page=limit, error_out=False)

        fundraisers = []
        for f in pagination.items:
            fundraisers.append({
                "id": f.id,
                "fundraiser_id": f.fundraiser_id,
                "title": f.title,
                "description": f.description,
                "goal_amount": f.goal_amount,
                "current_amount": f.current_amount,
                "image_url": f.image_url,
                "deadline": f.deadline.isoformat() if f.deadline else None,
                "created_at": f.created_at.isoformat() if f.created_at else None
            })

        response_data = {
            "total": pagination.total,
            "page": pagination.page,
            "pages": pagination.pages,
            "has_next": pagination.has_next,
            "has_prev": pagination.has_prev,
            "fundraisers": fundraisers
        }

        # Cache the response for future requests
        cache.set(cache_key, response_data, timeout=60 * 5)  # Cache for 5 minutes

        return response_data, 200

    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        data = fundraiser_parser.parse_args()

        fundraiser = Fundraiser(
            user_id=user_id,
            title=data["title"],
            description=data["description"],
            goal_amount=data["goal_amount"],
            image_url=data.get("image_url"),
            deadline=data.get("deadline")
        )
        db.session.add(fundraiser)
        db.session.commit()
        cache = current_app.cache
        # Invalidate cache after adding a new fundraiser
        cache.delete(f"user_fundraisers_{user_id}_page_1_limit_10")  # Clear cached fundraisers list

        return {
            "id": fundraiser.id,
            "fundraiser_id": fundraiser.fundraiser_id,
            "title": fundraiser.title,
            "description": fundraiser.description,
            "goal_amount": fundraiser.goal_amount,
            "current_amount": fundraiser.current_amount,
            "image_url": fundraiser.image_url,
            "deadline": fundraiser.deadline.isoformat() if fundraiser.deadline else None,
            "created_at": fundraiser.created_at.isoformat() if fundraiser.created_at else None
        }, 200


class FundraiserResource(Resource):
    @jwt_required()
    def get(self, fundraiser_id):
        user_id = get_jwt_identity()
        
        # Cache key for individual fundraiser
        cache_key = f"user_fundraiser_{user_id}_{fundraiser_id}"
        cache = current_app.cache
        # Try to get cached response
        cached_data = cache.get(cache_key)
        if cached_data:
            return cached_data, 200  # Return cached response if it exists

        fundraiser = Fundraiser.query.filter_by(fundraiser_id=fundraiser_id, user_id=user_id).first()
        if not fundraiser:
            return {"message": "Fundraiser not found"}, 404
        
        response_data = {
            "id": fundraiser.id,
            "fundraiser_id": fundraiser.fundraiser_id,
            "title": fundraiser.title,
            "description": fundraiser.description,
            "goal_amount": fundraiser.goal_amount,
            "current_amount": fundraiser.current_amount,
            "image_url": fundraiser.image_url,
            "deadline": fundraiser.deadline.isoformat() if fundraiser.deadline else None,
            "created_at": fundraiser.created_at.isoformat() if fundraiser.created_at else None
        }

        # Cache the response for future requests
        cache.set(cache_key, response_data, timeout=60 * 5)  # Cache for 5 minutes

        return response_data, 200

    @jwt_required()
    def put(self, fundraiser_id):
        user_id = get_jwt_identity()
        fundraiser = Fundraiser.query.filter_by(fundraiser_id=fundraiser_id, user_id=user_id).first()
        if not fundraiser:
            return {"message": "Fundraiser not found"}, 404

        data = fundraiser_parser.parse_args()
        # Only update fields that are provided in the request
        if data["title"]:
            fundraiser.title = data["title"]
        if data["description"]:
            fundraiser.description = data["description"]
        if data["goal_amount"]:
            fundraiser.goal_amount = data["goal_amount"]
        if data.get("image_url"):
            fundraiser.image_url = data["image_url"]
        if data.get("deadline"):
            fundraiser.deadline = data["deadline"]

        db.session.commit()
        cache = current_app.cache
        # Invalidate cache after updating a fundraiser
        cache.delete(f"user_fundraiser_{user_id}_{fundraiser_id}")  # Clear cached individual fundraiser
        cache.delete(f"user_fundraisers_{user_id}_page_1_limit_10")  # Clear cached list of fundraisers

        return {
            "id": fundraiser.id,
            "fundraiser_id": fundraiser.fundraiser_id,
            "title": fundraiser.title,
            "description": fundraiser.description,
            "goal_amount": fundraiser.goal_amount,
            "current_amount": fundraiser.current_amount,
            "image_url": fundraiser.image_url,
            "deadline": fundraiser.deadline.isoformat() if fundraiser.deadline else None,
            "created_at": fundraiser.created_at.isoformat() if fundraiser.created_at else None
        }, 200

    @jwt_required()
    def delete(self, fundraiser_id):
        user_id = get_jwt_identity()
        fundraiser = Fundraiser.query.filter_by(fundraiser_id=fundraiser_id, user_id=user_id).first()
        if not fundraiser:
            return {"message": "Fundraiser not found"}, 404

        db.session.delete(fundraiser)
        db.session.commit()

        # Invalidate cache after deleting a fundraiser
        cache = current_app.cache
        cache.delete(f"user_fundraiser_{user_id}_{fundraiser_id}")  # Clear cached individual fundraiser
        cache.delete(f"user_fundraisers_{user_id}_page_1_limit_10")  # Clear cached list of fundraisers

        return {"message": "Fundraiser deleted"}, 200
