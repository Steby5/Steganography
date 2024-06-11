document.getElementById('encodeForm').addEventListener('submit', async function(event) {
    event.preventDefault();
    const encodeImage = document.getElementById('encodeImage').files[0];
    const encodeMessage = document.getElementById('encodeMessage').value;
    const formData = new FormData();
    formData.append('image', encodeImage);
    formData.append('message', encodeMessage);

    const response = await fetch('/api/encode', {
        method: 'POST',
        body: formData
    });

    const result = await response.json();
    if (result.filename) {
        const encodedImageUrl = `/uploads/${result.filename}`;
        document.getElementById('encodedImage').src = encodedImageUrl;
        document.getElementById('downloadLink').href = encodedImageUrl;
        document.getElementById('encodedResult').style.display = 'block';
    }
});

document.getElementById('decodeForm').addEventListener('submit', async function(event) {
    event.preventDefault();
    const decodeImage = document.getElementById('decodeImage').files[0];
    const formData = new FormData();
    formData.append('image', decodeImage);

    const response = await fetch('/api/decode', {
        method: 'POST',
        body: formData
    });

    const result = await response.json();
    if (result.message) {
        document.getElementById('decodedMessage').innerText = result.message;
        document.getElementById('decodedResult').style.display = 'block';
    }
});
