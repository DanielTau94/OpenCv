function setColor() {
    const colorSelect = document.getElementById('colorSelect');
    const color = colorSelect.value;

    fetch('/set_color', {
        method: 'POST',
        body: JSON.stringify({ color }),
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.error(error));
}

function setSize() {
    const widthInput = document.getElementById('widthInput');
    const heightInput = document.getElementById('heightInput');
    const width = widthInput.value;
    const height = heightInput.value;

    fetch('/set_size', {
        method: 'POST',
        body: JSON.stringify({ width, height }),
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.error(error));
}

function startOneVideoStream() {
    const videoContainer = document.getElementById('videoContainer');
    videoContainer.innerHTML = '<img id="videoStream" src="/start_one_video_stream" alt="Video Stream">';
}

function startTwoVideoStreams() {
    const videoContainer = document.getElementById('videoContainer');
    videoContainer.innerHTML = '<img id="videoStream" src="/start_two_video_streams" alt="Video Stream">';
}

document.getElementById('oneVideoBtn').addEventListener('click', startOneVideoStream);
document.getElementById('twoVideosBtn').addEventListener('click', startTwoVideoStreams);
document.getElementById('setColorBtn').addEventListener('click', setColor);
document.getElementById('setSizeBtn').addEventListener('click', setSize);

startOneVideoStream(); 