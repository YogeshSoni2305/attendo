const video = document.getElementById('video');
const captureBtn = document.getElementById('capture-btn');
const resultDiv = document.getElementById('result');

navigator.mediaDevices.getUserMedia({ video: true })
  .then(stream => {
    video.srcObject = stream;
  });

captureBtn.addEventListener('click', async () => {
  const canvas = document.createElement('canvas');
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  canvas.getContext('2d').drawImage(video, 0, 0);

  const blob = await new Promise(resolve => canvas.toBlob(resolve, 'image/jpeg'));

  const formData = new FormData();
  formData.append('frame', blob, 'capture.jpg');

  const res = await fetch('/process_frame', {
    method: 'POST',
    body: formData
  });

  const data = await res.json();
  resultDiv.textContent = data.message;
});
function sendEmail() {
    fetch('/send_email', {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

