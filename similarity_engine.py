"""
Image Similarity Engine using Deep Learning.
Utilizes pre-trained ResNet50 for feature extraction and cosine similarity for comparison.
"""

import numpy as np
from PIL import Image
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input
from tensorflow.keras.preprocessing import image
from sklearn.metrics.pairwise import cosine_similarity
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ImageSimilarityEngine:
    """
    Compute similarity between two images using deep learning.
    Uses ResNet50 for feature extraction and cosine similarity for comparison.
    """

    def __init__(self, model_name='resnet50'):
        """
        Initialize the similarity engine with a pre-trained model.

        Args:
            model_name (str): Name of the pre-trained model to use
        """
        self.model_name = model_name
        self.model = None
        self.img_size = (224, 224)
        self._load_model()

    def _load_model(self):
        """Load the pre-trained ResNet50 model without top classification layer."""
        try:
            logger.info(f"Loading {self.model_name} model...")
            self.model = ResNet50(
                weights='imagenet',
                include_top=False,
                pooling='avg',
                input_shape=(224, 224, 3)
            )
            logger.info("Model loaded successfully")
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            raise

    def _load_and_preprocess_image(self, img_path):
        """
        Load and preprocess an image for model input.

        Args:
            img_path (str): Path to the image file

        Returns:
            np.array: Preprocessed image array
        """
        try:
            img = Image.open(img_path).convert('RGB')
            img = img.resize(self.img_size, Image.LANCZOS)
            img_array = image.img_to_array(img)
            img_array = np.expand_dims(img_array, axis=0)
            img_array = preprocess_input(img_array)
            return img_array
        except Exception as e:
            logger.error(f"Error preprocessing image {img_path}: {str(e)}")
            raise

    def _extract_features(self, img_path):
        """
        Extract deep learning features from an image.

        Args:
            img_path (str): Path to the image file

        Returns:
            np.array: Feature vector extracted from the image
        """
        try:
            preprocessed_img = self._load_and_preprocess_image(img_path)
            features = self.model.predict(preprocessed_img, verbose=0)
            return features.flatten()
        except Exception as e:
            logger.error(f"Error extracting features: {str(e)}")
            raise

    def compute_similarity(self, img1_path, img2_path):
        """
        Compute similarity between two images.

        Args:
            img1_path (str): Path to first image
            img2_path (str): Path to second image

        Returns:
            dict: Dictionary containing similarity score and metadata
        """
        try:
            logger.info(f"Computing similarity between {img1_path} and {img2_path}")

            # Extract features from both images
            features1 = self._extract_features(img1_path)
            features2 = self._extract_features(img2_path)

            # Reshape for cosine similarity
            features1 = features1.reshape(1, -1)
            features2 = features2.reshape(1, -1)

            # Compute cosine similarity
            similarity = cosine_similarity(features1, features2)[0][0]

            # Convert to percentage
            similarity_percentage = float(similarity * 100)

            # Determine similarity level
            if similarity_percentage >= 80:
                level = "Very High"
            elif similarity_percentage >= 60:
                level = "High"
            elif similarity_percentage >= 40:
                level = "Moderate"
            elif similarity_percentage >= 20:
                level = "Low"
            else:
                level = "Very Low"

            result = {
                'similarity_score': round(similarity_percentage, 2),
                'similarity_level': level,
                'raw_score': float(similarity),
                'status': 'success'
            }

            logger.info(f"Similarity computed: {similarity_percentage:.2f}%")
            return result

        except Exception as e:
            logger.error(f"Error computing similarity: {str(e)}")
            return {
                'status': 'error',
                'message': str(e),
                'similarity_score': 0
            }

    def batch_compare(self, reference_img, comparison_imgs):
        """
        Compare a reference image against multiple images.

        Args:
            reference_img (str): Path to reference image
            comparison_imgs (list): List of paths to comparison images

        Returns:
            list: List of similarity results
        """
        results = []
        ref_features = self._extract_features(reference_img)

        for comp_img in comparison_imgs:
            try:
                comp_features = self._extract_features(comp_img)
                similarity = cosine_similarity(
                    ref_features.reshape(1, -1),
                    comp_features.reshape(1, -1)
                )[0][0]

                results.append({
                    'image': comp_img,
                    'similarity': float(similarity * 100)
                })
            except Exception as e:
                logger.error(f"Error comparing {comp_img}: {str(e)}")
                results.append({
                    'image': comp_img,
                    'similarity': 0,
                    'error': str(e)
                })

        return sorted(results, key=lambda x: x['similarity'], reverse=True)


def get_similarity_engine():
    """Factory function to get or create a similarity engine instance."""
    if not hasattr(get_similarity_engine, 'engine'):
        get_similarity_engine.engine = ImageSimilarityEngine()
    return get_similarity_engine.engine
