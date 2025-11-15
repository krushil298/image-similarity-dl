# Image Similarity Comparison System

A deep learning-powered web application that compares two images and computes their similarity score using pre-trained convolutional neural networks.

## Features

- **Modern Glassmorphism UI** - Beautiful gradient background with animated floating elements
- **Drag & Drop Upload** - Intuitive image upload with preview
- **Deep Learning Analysis** - Powered by pre-trained ResNet50 model
- **Circular Progress Visualization** - Animated score ring with gradient effects
- **Real-time Results** - Instant similarity scoring with detailed explanations
- **Fully Responsive** - Works seamlessly on desktop, tablet, and mobile devices

## Technologies Used

### Backend
- **Python 3.8+**
- **Flask** - Web framework
- **TensorFlow/Keras** - Deep learning framework
- **Pillow** - Image processing
- **NumPy** - Numerical computations

### Frontend
- **HTML5/CSS3**
- **JavaScript**
- **Bootstrap 5** - UI framework

### Deep Learning Model
- **ResNet50** - Pre-trained on ImageNet for feature extraction
- **Cosine Similarity** - For comparing image embeddings

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup Instructions

1. Clone the repository:
```bash
git clone <repository-url>
cd image-similarity-comparison
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python app.py
```

5. Open browser and navigate to:
```
http://localhost:5000
```

## Usage

1. Click on "Choose Image 1" to upload your first image
2. Click on "Choose Image 2" to upload your second image
3. Click "Compare Images" button
4. View the similarity percentage and visual comparison

## Project Structure

```
image-similarity-comparison/
├── app.py                  # Main Flask application
├── similarity_engine.py    # Image similarity computation logic
├── requirements.txt        # Python dependencies
├── README.md              # Project documentation
├── .gitignore            # Git ignore rules
├── .clauderules          # Code quality standards
├── static/
│   ├── css/
│   │   └── style.css     # Custom styles
│   ├── js/
│   │   └── main.js       # Frontend logic
│   └── images/           # Static images
├── templates/
│   └── index.html        # Main HTML template
├── uploads/              # Temporary upload directory
└── models/               # Cached models (gitignored)
```

## How It Works

1. **Image Upload**: Users upload two images through the web interface
2. **Preprocessing**: Images are resized and normalized to 224x224 pixels
3. **Feature Extraction**: ResNet50 extracts high-level features from both images
4. **Similarity Computation**: Cosine similarity is calculated between feature vectors
5. **Result Display**: Similarity score (0-100%) is shown with visual feedback

## API Endpoints

### POST /compare
Compares two uploaded images

**Request:**
- Method: POST
- Content-Type: multipart/form-data
- Body: image1, image2 (file uploads)

**Response:**
```json
{
  "similarity": 85.5,
  "message": "Images are highly similar",
  "image1_url": "/uploads/img1.jpg",
  "image2_url": "/uploads/img2.jpg"
}
```

## Performance

- Average processing time: 2-4 seconds per comparison
- Supported image formats: JPG, JPEG, PNG
- Maximum file size: 16MB per image

## Future Enhancements

- Support for multiple similarity algorithms (SSIM, MSE, etc.)
- Batch comparison of multiple images
- Image history and comparison logs
- Advanced visualization (heatmaps, difference maps)
- Mobile app version

## Course Information

- **Course**: Essentials of Deep Learning (23CSE116)
- **Assignment**: Image Similarity Comparison Website
- **Deadline**: 25/10/2025

## License

This project is created for educational purposes as part of the Deep Learning course assignment.

## Contributors

[Add your names here]

## Acknowledgments

- Pre-trained ResNet50 model from Keras Applications
- TensorFlow and Keras teams
- Bootstrap for UI components
