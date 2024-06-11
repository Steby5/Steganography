# Steganography SPA

This project is a Single Page Application (SPA) for steganography, which allows you to encode and decode secret messages in images. The application uses Flask for the backend, SQLite for the database, and HTML, CSS, and JavaScript for the frontend.

## Features

- Encode a secret message into an image.
- Decode a secret message from an image.
- Support for JPG, JPEG, and PNG image formats.
- SPA interface for seamless user experience.
- Dockerized for easy deployment.

## Prerequisites

- Docker

## Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/Steby5/Steganography.git
    cd Steganography
    ```

2. **Build the Docker image:**
    ```bash
    docker build -t steganography_app .
    ```

3. **Run the Docker container:**
    ```bash
    docker run -p 5000:5000 -v $(pwd)/uploads:/usr/src/app/uploads -v $(pwd)/outputs:/usr/src/app/outputs steganography_app
    ```

## Usage

1. Open your web browser and go to `http://127.0.0.1:5000/`.
2. Use the "Encode Message" section to upload an image and enter a secret message. The encoded image will be displayed, and you can download it.
3. Use the "Decode Message" section to upload an encoded image and view the secret message.

## Project Structure
```
Steganography/
├── app.py
├── requirements.txt
├── Dockerfile
├── templates/
│ └── index.html
├── static/
│ ├── style.css
│ └── script.js
├── uploads/
├── outputs/
```

- `app.py`: The Flask application code.
- `requirements.txt`: List of Python dependencies.
- `Dockerfile`: Dockerfile to create a Docker image.
- `templates/`: Folder containing HTML templates.
- `static/`: Folder containing static files (CSS, JavaScript).
- `uploads/`: Folder to store uploaded images.
- `outputs/`: Folder to store encoded images.

## API Endpoints

- `POST /api/encode`: Encode a message into an image.
    - Request:
        - `image`: The image file to encode the message into.
        - `message`: The secret message to encode.
    - Response:
        - `filename`: The filename of the encoded image.
- `POST /api/decode`: Decode a message from an image.
    - Request:
        - `image`: The encoded image file.
    - Response:
        - `message`: The decoded secret message.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Flask](https://flask.palletsprojects.com/)
- [Pillow](https://python-pillow.org/)
- [SQLite](https://www.sqlite.org/index.html)
