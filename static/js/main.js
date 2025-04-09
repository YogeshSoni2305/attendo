// const video = document.getElementById('video');
// const captureBtn = document.getElementById('capture-btn');
// const resultDiv = document.getElementById('result');

// navigator.mediaDevices.getUserMedia({ video: true })
//   .then(stream => {
//     video.srcObject = stream;
//   });

// captureBtn.addEventListener('click', async () => {
//   const canvas = document.createElement('canvas');
//   canvas.width = video.videoWidth;
//   canvas.height = video.videoHeight;
//   canvas.getContext('2d').drawImage(video, 0, 0);

//   const blob = await new Promise(resolve => canvas.toBlob(resolve, 'image/jpeg'));

//   const formData = new FormData();
//   formData.append('frame', blob, 'capture.jpg');

//   const res = await fetch('/process_frame', {
//     method: 'POST',
//     body: formData
//   });

//   const data = await res.json();
//   resultDiv.textContent = data.message;
// });
// function sendEmail() {
//     fetch('/send_email', {
//         method: 'POST'
//     })
//     .then(response => response.json())
//     .then(data => {
//         alert(data.message);
//     })
//     .catch(error => {
//         console.error('Error:', error);
//     });
// }


const video = document.getElementById('video');
const captureBtn = document.getElementById('capture-btn');
const resultDiv = document.getElementById('result');

navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => {
        video.srcObject = stream;
    })
    .catch(err => {
        console.error("Error accessing webcam: ", err);
        resultDiv.textContent = "Error: Could not access webcam.";
        resultDiv.style.color = "#dc3545"; // Red for error
    });

captureBtn.addEventListener('click', async () => {
    resultDiv.textContent = "Processing..."; // Show loading state
    resultDiv.style.color = "#6c757d"; // Gray for processing

    const canvas = document.createElement('canvas');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    canvas.getContext('2d').drawImage(video, 0, 0);

    const blob = await new Promise(resolve => canvas.toBlob(resolve, 'image/jpeg'));

    const formData = new FormData();
    formData.append('frame', blob, 'capture.jpg');

    try {
        const res = await fetch('/process_frame', {
            method: 'POST',
            body: formData
        });

        const data = await res.json();
        resultDiv.textContent = data.message;
        resultDiv.style.color = data.status === 'success' ? '#28a745' : '#dc3545'; // Green for success, Red for error
    } catch (error) {
        resultDiv.textContent = "Error: Failed to process frame.";
        resultDiv.style.color = "#dc3545";
        console.error('Error:', error);
    }
});

function sendEmail() {
    fetch('/send_email', {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        if (data.message.includes('Sent!')) {
            resultDiv.textContent = "Attendance email sent successfully!";
            resultDiv.style.color = "#28a745";
        } else {
            resultDiv.textContent = "Failed to send email.";
            resultDiv.style.color = "#dc3545";
        }
    })
    .catch(error => {
        resultDiv.textContent = "Error: Failed to send email.";
        resultDiv.style.color = "#dc3545";
        console.error('Error:', error);
    });
}



