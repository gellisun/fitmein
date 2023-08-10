
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

    window.location.assign(`https://fit-me-in-7fcf0f4ba962.herokuapp.com/my_match/${latitude}/${longitude}/`)
    // window.location.assign(`http://localhost:8000/my_match/${latitude}/${longitude}/`)

}

function error() {
    console.log('error')
    alert("Unable to retrieve your location.");
}