

const displayCoord = document.getElementById("displayCoord")
const latitudeDisplay = document.getElementById("latitude")
const longitudeDisplay = document.getElementById("longitude")

displayCoord.addEventListener("click", getLocation)

function getLocation() {
    console.log('click')
    if ("geolocation" in navigator) {
        navigator.geolocation.getCurrentPosition(success, error);
    } else {
        alert("Geolocation is not available in your browser.");
    }
}

function success(position) {
    const latitude = position.coords.latitude;
    const longitude = position.coords.longitude;
    console.log('success')
    console.log(latitude)
    // latitudeDisplay.innerHTML = latitude
    // longitudeDisplay.innerHTML = longitude

    sendToServer(latitude, longitude)
}

function error() {
    console.log('error')
    alert("Unable to retrieve your location.");
}

// Function to get CSRF token from cookies
function getCookie(name) {
    const cookieValue = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
    return cookieValue ? cookieValue.pop() : '';
}

function sendToServer(latitude, longitude){
    const data = { 'latitude': latitude, 'longitude': longitude };
    
    fetch('/match/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body: JSON.stringify(data),
    })
    console.log('checkpoint 1')
        .then(response => {
            if (response.ok) {
                console.log('Location data sent successfully.');
            } else {
                console.error('Failed to send location data to server.');
            }
        })
        .catch(error => {
            console.error('Error sending location data:', error);
        });
}