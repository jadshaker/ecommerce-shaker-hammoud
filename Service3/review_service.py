from database_utils.connect import get_supabase_client
from models.review import Review

class ReviewService:
    def __init__(self):
        self.supabase = get_supabase_client()
        self.reviews_table = 'review'

    def submit_review(self, review_data):
        """
        Submit a new review for a product
        """
        try:
            response = self.supabase.table(self.reviews_table).insert(review_data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            raise ValueError(f"Error submitting review: {str(e)}")

    def update_review(self, review_id, update_data):
        """
        Update an existing review
        """
        try:
            response = (self.supabase.table(self.reviews_table)
                        .update(update_data)
                        .eq('review_id', review_id)
                        .execute())
            return response.data[0] if response.data else None
        except Exception as e:
            raise ValueError(f"Error updating review: {str(e)}")

    def delete_review(self, review_id):
        """
        Delete a review by its ID
        """
        try:
            response = (self.supabase.table(self.reviews_table)
                        .delete()
                        .eq('review_id', review_id)
                        .execute())
            return response.data if response.data else None
        except Exception as e:
            raise ValueError(f"Error deleting review: {str(e)}")

    def get_product_reviews(self, product_id):
        """
        Retrieve all reviews for a specific product
        """
        try:
            response = (self.supabase.table(self.reviews_table)
                        .select('*')
                        .eq('product_id', product_id)
                        .execute())
            return response.data if response.data else []
        except Exception as e:
            raise ValueError(f"Error retrieving product reviews: {str(e)}")

    def get_customer_reviews(self, customer_id):
        """
        Retrieve all reviews submitted by a specific customer
        """
        try:
            response = (self.supabase.table(self.reviews_table)
                        .select('*')
                        .eq('customer_id', customer_id)
                        .execute())
            return response.data if response.data else []
        except Exception as e:
            raise ValueError(f"Error retrieving customer reviews: {str(e)}")

    def moderate_review(self, review_id, moderation_status):
        """
        Moderate a review (flag or approve)
        """
        try:
            response = (self.supabase.table(self.reviews_table)
                        .update({'moderation_status': moderation_status})
                        .eq('id', review_id)
                        .execute())
            return response.data[0] if response.data else None
        except Exception as e:
            raise ValueError(f"Error moderating review: {str(e)}")

    def get_review_details(self, review_id):
        """
        Get detailed information about a specific review
        """
        try:
            response = (self.supabase.table(self.reviews_table)
                        .select('*')
                        .eq('id', review_id)
                        .execute())
            return response.data[0] if response.data else None
        except Exception as e:
            raise ValueError(f"Error retrieving review details: {str(e)}")
