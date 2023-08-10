
const displayCoord = document.getElementById("displayCoord")
const latitudeDisplay = document.getElementById("latitude")
const longitudeDisplay = document.getElementById("longitude")

displayCoord.addEventListener("click", getLocation)

function getLocation(event) {
    event.preventDefault()
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

    window.location.assign(`http://localhost:8000/my_match/${latitude}/${longitude}/`)
    // sendToServer(latitude, longitude)
}

function error() {
    console.log('error')
    alert("Unable to retrieve your location.");
}

// Function to get CSRF token from cookies
function getCsrf(csrf) {
    const cookieValue = document.cookie.match('(^|;)\\s*' + csrf + '\\s*=\\s*([^;]+)');
    return cookieValue ? cookieValue.pop() : '';
}
console.log(getCsrf('csrftoken'))

function sendToServer(latitude, longitude){
    const data = { 'latitude': latitude, 'longitude': longitude };
    
    fetch('/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCsrf('csrftoken'),
        },
        body: JSON.stringify(data),
    })
        .then((response) => {
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