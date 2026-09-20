// ==========================================
// Smart Simhastha 2028 - Smart Map
// Leaflet + OpenStreetMap
// ==========================================

// Ujjain coordinates
const UJJAIN = [23.1765, 75.7885];

// Create map
const map = L.map("map").setView(UJJAIN, 13);

// OpenStreetMap
L.tileLayer(
    "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
    {
        maxZoom: 19,
        attribution: "&copy; OpenStreetMap contributors"
    }
).addTo(map);


// ==========================================
// Ujjain Marker
// ==========================================

const ujjainMarker = L.marker(UJJAIN)
    .addTo(map)
    .bindPopup(`
        <b>🕉️ Ujjain</b><br>
        Smart Simhastha 2028
    `);


// ==========================================
// User Location
// ==========================================

let userMarker = null;
let accuracyCircle = null;

function saveUserLocation(latitude, longitude, accuracy) {
    localStorage.setItem("simhasthaUserLocation", JSON.stringify({ latitude, longitude, accuracy, savedAt: Date.now() }));
    window.dispatchEvent(new CustomEvent("simhastha:location", { detail: { latitude, longitude, accuracy } }));
}


function findMyLocation() {

    const message =
        document.getElementById("location-message");

    if (!navigator.geolocation) {

        showMessage(
            "❌ Your browser does not support location services.",
            "danger"
        );

        return;
    }


    showMessage(
        "📍 Getting your location...",
        "warning"
    );


    navigator.geolocation.getCurrentPosition(

        function(position) {

            const latitude =
                position.coords.latitude;

            const longitude =
                position.coords.longitude;

            const accuracy =
                position.coords.accuracy;


            const userLocation = [
                latitude,
                longitude
            ];

            saveUserLocation(latitude, longitude, accuracy);


            // Remove previous marker
            if (userMarker) {

                map.removeLayer(userMarker);
            }


            // Remove previous accuracy circle
            if (accuracyCircle) {

                map.removeLayer(accuracyCircle);
            }


            // Create user marker
            userMarker = L.marker(userLocation)
                .addTo(map)
                .bindPopup(`
                    <b>📍 You are here</b><br>
                    Accuracy: approximately
                    ${Math.round(accuracy)} meters
                `)
                .openPopup();


            // Accuracy circle
            accuracyCircle = L.circle(
                userLocation,
                {
                    radius: accuracy
                }
            ).addTo(map);


            // Move map to user
            map.setView(
                userLocation,
                16
            );


            showMessage(
                "✅ आपका वर्तमान स्थान मिल गया है। इसे इस ब्राउज़र में सुरक्षित रखा गया है।",
                "success"
            );
        },


        function(error) {

            let errorMessage;


            switch (error.code) {

                case error.PERMISSION_DENIED:

                    errorMessage =
                        "Location permission was denied.";

                    break;


                case error.POSITION_UNAVAILABLE:

                    errorMessage =
                        "Location information is unavailable.";

                    break;


                case error.TIMEOUT:

                    errorMessage =
                        "Location request timed out.";

                    break;


                default:

                    errorMessage =
                        "Unable to get your location.";
            }


            showMessage(
                "⚠️ " + errorMessage,
                "danger"
            );
        },


        {
            enableHighAccuracy: true,
            timeout: 10000,
            maximumAge: 0
        }
    );
}


// ==========================================
// Return to Ujjain
// ==========================================

function showUjjain() {

    map.setView(
        UJJAIN,
        13
    );


    ujjainMarker
        .bindPopup(`
            <b>🕉️ Ujjain</b><br>
            Smart Simhastha 2028
        `)
        .openPopup();
}


// ==========================================
// Message Function
// ==========================================

function showMessage(
    text,
    type
) {

    const message =
        document.getElementById(
            "location-message"
        );


    message.style.display =
        "block";


    message.className =
        "alert " + type;


    message.innerText =
        text;
}