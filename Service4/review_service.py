from database_utils.connect import get_supabase_client


class ReviewService:
    """
    A service class for managing product reviews in the Supabase database.

    Methods:
        __init__():
            Initializes the ReviewService instance, setting up the Supabase client and reviews table name.

        submit_review(review_data):
            Submits a new review for a product.
            Args:
                review_data (dict): The data of the review to be submitted.
            Returns:
                dict: The submitted review data if successful, None otherwise.
            Raises:
                ValueError: If there is an error submitting the review.

        update_review(review_id, update_data):
            Updates an existing review.
            Args:
                review_id (int): The ID of the review to be updated.
                update_data (dict): The data to update the review with.
            Returns:
                dict: The updated review data if successful, None otherwise.
            Raises:
                ValueError: If there is an error updating the review.

        delete_review(review_id):
            Deletes a review by its ID.
            Args:
                review_id (int): The ID of the review to be deleted.
            Returns:
                list: The data of the deleted review if successful, None otherwise.
            Raises:
                ValueError: If there is an error deleting the review.

        get_product_reviews(product_id):
            Retrieves all reviews for a specific product.
            Args:
                product_id (int): The ID of the product to retrieve reviews for.
            Returns:
                list: A list of reviews for the specified product.
            Raises:
                ValueError: If there is an error retrieving the product reviews.

        get_customer_reviews(customer_id):
            Retrieves all reviews submitted by a specific customer.
            Args:
                customer_id (int): The ID of the customer to retrieve reviews for.
            Returns:
                list: A list of reviews submitted by the specified customer.
            Raises:
                ValueError: If there is an error retrieving the customer reviews.

        moderate_review(review_id, moderation_status):
            Moderates a review (flag or approve).
            Args:
                review_id (int): The ID of the review to be moderated.
                moderation_status (str): The moderation status to set for the review.
            Returns:
                dict: The moderated review data if successful, None otherwise.
            Raises:
                ValueError: If there is an error moderating the review.

        get_review_details(review_id):
            Retrieves detailed information about a specific review.
            Args:
                review_id (int): The ID of the review to retrieve details for.
            Returns:
                dict: The detailed review data if successful, None otherwise.
            Raises:
                ValueError: If there is an error retrieving the review details.
    """

    def __init__(self):
        """
        Initializes the ReviewService instance.

        This constructor sets up the connection to the Supabase client and specifies
        the reviews table name.

        Attributes:
            supabase: The Supabase client instance used to interact with the database.
            reviews_table (str): The name of the table where reviews are stored.
        """
        self.supabase = get_supabase_client()
        self.reviews_table = "review"

    def submit_review(self, review_data):
        """
        Submit a new review for a product
        """
        try:
            response = (
                self.supabase.table(self.reviews_table).insert(review_data).execute()
            )
            return response.data[0] if response.data else None
        except Exception as e:
            raise ValueError(f"Error submitting review: {str(e)}")

    def update_review(self, review_id, update_data):
        """
        Update an existing review
        """
        try:
            response = (
                self.supabase.table(self.reviews_table)
                .update(update_data)
                .eq("review_id", review_id)
                .execute()
            )
            return response.data[0] if response.data else None
        except Exception as e:
            raise ValueError(f"Error updating review: {str(e)}")

    def delete_review(self, review_id):
        """
        Delete a review by its ID
        """
        try:
            response = (
                self.supabase.table(self.reviews_table)
                .delete()
                .eq("review_id", review_id)
                .execute()
            )
            return response.data if response.data else None
        except Exception as e:
            raise ValueError(f"Error deleting review: {str(e)}")

    def get_product_reviews(self, product_id):
        """
        Retrieve all reviews for a specific product
        """
        try:
            response = (
                self.supabase.table(self.reviews_table)
                .select("*")
                .eq("product_id", product_id)
                .execute()
            )
            return response.data if response.data else []
        except Exception as e:
            raise ValueError(f"Error retrieving product reviews: {str(e)}")

    def get_customer_reviews(self, customer_id):
        """
        Retrieve all reviews submitted by a specific customer
        """
        try:
            response = (
                self.supabase.table(self.reviews_table)
                .select("*")
                .eq("customer_id", customer_id)
                .execute()
            )
            return response.data if response.data else []
        except Exception as e:
            raise ValueError(f"Error retrieving customer reviews: {str(e)}")

    def moderate_review(self, review_id, moderation_status):
        """
        Moderate a review (flag or approve)
        """
        try:
            response = (
                self.supabase.table(self.reviews_table)
                .update({"moderation_status": moderation_status})
                .eq("id", review_id)
                .execute()
            )
            return response.data[0] if response.data else None
        except Exception as e:
            raise ValueError(f"Error moderating review: {str(e)}")

    def get_review_details(self, review_id):
        """
        Get detailed information about a specific review
        """
        try:
            response = (
                self.supabase.table(self.reviews_table)
                .select("*")
                .eq("id", review_id)
                .execute()
            )
            return response.data[0] if response.data else None
        except Exception as e:
            raise ValueError(f"Error retrieving review details: {str(e)}")
