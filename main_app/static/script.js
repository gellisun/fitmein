
document.addEventListener("DOMContentLoaded", loadContent); 

function loadContent() {
    const form = document.getElementById("locationForm");
    form.submit();

    function getLocation() {
        if ("geolocation" in navigator) {
            navigator.geolocation.getCurrentPosition(success, error);
        } else {
            alert("Geolocation is not available in your browser.");
        }
    }

    function success(position) {
        const latitude = position.coords.latitude;
        const longitude = position.coords.longitude;
        const latitudeField = document.getElementById("latitudeInput");
        const longitudeField = document.getElementById("longitudeInput");

        latitudeField.value = latitude;
        longitudeField.value = longitude;
        
        form.submit();
    }

    function error() {
        alert("Unable to retrieve your location.");
    }

    const linkToMatch = document.getElementById("linkToMatch");
    linkToMatch.addEventListener("click", function (event) {
        event.preventDefault();
        getLocation();
    });
};
