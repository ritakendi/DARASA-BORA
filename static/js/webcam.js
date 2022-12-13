document.addEventListener('DOMContentLoaded', e => {
    // Check if the browser supports the getUserMedia() method
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        // Get the video and capture button elements
        var video = document.getElementById('webcam-container');
        var captureButton = document.getElementById('signin');

        // Request access to the webcam
        navigator.mediaDevices.getUserMedia({ video: true, audio: false })
            .then(function (stream) {
                // Set the source of the video element to the webcam stream
                video.srcObject = stream;

                // Start the video
                video.autoplay = true;

                // Add a click event listener to the capture button
                captureButton.addEventListener('click', function () {
                    // Create a canvas element to draw the webcam image on
                    var canvas = document.createElement('canvas');
                    var context = canvas.getContext('2d');

                    // Set the width and height of the canvas to match the video
                    canvas.width = video.videoWidth;
                    canvas.height = video.videoHeight;

                    // Draw the current frame of the video on the canvas
                    context.drawImage(video, 0, 0, canvas.width, canvas.height);

                    // Get the image data from the canvas as a Data URL
                    var dataURL = canvas.toDataURL();

                    // Use the Data URL for further processing, such as verification
                    // ...
                    console.log(dataURL)

                    var username = document.getElementById('user_signin').value
                    var password = document.getElementById('pass_signin').value

                    console.log(username, password)

                    fetch('/signin', {
                        method: 'POST',
                        headers: {
                            'Accept': 'application/json',
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({
                            username: username,
                            password: password,
                            user_photo: dataURL
                        })
                    })
                        .then(response => response.json())
                        .then(response => console.log(response.image))




                });
            })
            .catch(function (err) {
                // Handle any errors
                console.log("Error: " + err);
            });
    }
})