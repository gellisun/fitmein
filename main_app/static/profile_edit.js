document.addEventListener('DOMContentLoaded', function () {
    const profileId = '{{ profile.id }}'; // Replace with the actual profile ID
    const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
    const editableFields = document.querySelectorAll('.editable-field');

    // Function to handle updating the profile data via AJAX
    function updateProfileData(fieldId, newValue) {
        const data = {
            'field_id': fieldId,
            'new_value': newValue,
            'csrfmiddlewaretoken': csrfToken,
        };

        const xhr = new XMLHttpRequest();
        xhr.open('POST', '/update_profile/' + profileId + '/', true);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.onload = function () {
            if (xhr.status === 200) {
                // Data updated successfully, do something if needed
            } else {
                // Error occurred, handle the error if needed
            }
        };
        xhr.send(JSON.stringify(data));
    }

    // Function to handle editing the contenteditable fields
    function handleFieldEditing(event) {
        const fieldElement = event.target;
        const fieldId = fieldElement.dataset.fieldName;
        const newValue = fieldElement.innerText;
        updateProfileData(fieldId, newValue);
    }

    // Function to retrieve profile data from the server and populate the contenteditable fields
    function loadProfileData() {
        const xhr = new XMLHttpRequest();
        xhr.open('GET', '/get_profile_data/' + profileId + '/', true);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.onload = function () {
            if (xhr.status === 200) {
                const data = JSON.parse(xhr.responseText);
                document.getElementById('location').innerText = data.location;
                document.getElementById('favorites').innerText = data.favorites;
            } else {
                // Error occurred, handle the error if needed
            }
        };
        xhr.send();
    }

    // Add click event listeners to the editable fields
    editableFields.forEach((field) => {
        field.addEventListener('blur', handleFieldEditing);
    });

    // Load profile data when the page loads
    loadProfileData();
});