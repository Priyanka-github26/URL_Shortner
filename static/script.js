/* ========================= */
/* GLOBAL URL DATA */
/* ========================= */

let allURLs = [];


/* ========================= */
/* SHORTEN URL */
/* ========================= */

async function shortenURL() {

    const urlInput =
        document.getElementById("urlInput");

    const resultBox =
        document.getElementById("resultBox");

    const errorMessage =
        document.getElementById("errorMessage");

    const shortURL =
        document.getElementById("shortURL");

    const shortenButton =
        document.getElementById("shortenButton");


    const url =
        urlInput.value.trim();


    // Clear previous messages

    errorMessage.style.display = "none";

    resultBox.style.display = "none";


    // Check empty URL

    if (!url) {

        errorMessage.textContent =
            "Please enter a URL.";

        errorMessage.style.display =
            "block";

        return;

    }


    try {

        // Loading state

        shortenButton.disabled = true;

        shortenButton.textContent =
            "Shortening...";


        const response =
            await fetch("/shorten", {

                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json"
                },

                body: JSON.stringify({
                    url: url
                })

            });


        const data =
            await response.json();


        // Handle API error

        if (!response.ok) {

            errorMessage.textContent =
                data.error ||
                "Something went wrong.";

            errorMessage.style.display =
                "block";

            return;

        }


        // Display shortened URL

        shortURL.textContent =
            data.short_url;

        resultBox.style.display =
            "block";


        // Clear input

        urlInput.value = "";


        // Refresh dashboard

        loadURLs();


        console.log(
            "API Response:",
            data
        );

    }


    catch (error) {

        console.error(error);

        errorMessage.textContent =
            "Unable to connect to the server.";

        errorMessage.style.display =
            "block";

    }


    finally {

        // Restore button

        shortenButton.disabled = false;

        shortenButton.textContent =
            "Shorten URL";

    }

}


/* ========================= */
/* COPY URL */
/* ========================= */

function copyURL() {

    const url =
        document
            .getElementById("shortURL")
            .textContent;


    navigator.clipboard.writeText(url)
        .then(function() {

            alert("URL copied!");

        })
        .catch(function(error) {

            console.error(error);

            alert("Unable to copy URL.");

        });

}


/* ========================= */
/* LOAD ALL URLS */
/* ========================= */

async function loadURLs() {

    const tableBody =
        document.getElementById(
            "urlTableBody"
        );


    tableBody.innerHTML = `

        <tr>

            <td
                colspan="6"
                class="no-data">

                Loading...

            </td>

        </tr>

    `;


    try {

        const response =
            await fetch("/urls");


        const data =
            await response.json();


        if (!response.ok) {

            throw new Error(
                data.error ||
                "Unable to load URLs"
            );

        }


        // Store URLs globally

        allURLs = data.urls;


        // Update analytics

        updateAnalytics(allURLs);


        // Display URLs

        displayURLs(allURLs);

    }


    catch (error) {

        console.error(error);


        tableBody.innerHTML = `

            <tr>

                <td
                    colspan="6"
                    class="no-data">

                    ❌ Unable to load URLs

                </td>

            </tr>

        `;

    }

}


/* ========================= */
/* DISPLAY URLS */
/* ========================= */

function displayURLs(urls) {

    const tableBody =
        document.getElementById(
            "urlTableBody"
        );


    tableBody.innerHTML = "";


    // No URLs

    if (!urls || urls.length === 0) {

        tableBody.innerHTML = `

            <tr>

                <td
                    colspan="6"
                    class="no-data">

                    No URLs found.

                </td>

            </tr>

        `;

        return;

    }


    // Display each URL

    urls.forEach(function(url) {

        const row =
            document.createElement("tr");


        row.innerHTML = `

            <td>

                <a
                    href="/${url.short_code}"
                    target="_blank"
                    class="short-link">

                    /${url.short_code}

                </a>

            </td>


            <td>

                ${truncateURL(
                    url.original_url
                )}

            </td>


            <td>

                📊 ${url.clicks}

            </td>


            <td>

                ${formatDate(
                    url.created_at
                )}

            </td>


            <td>

                ${getExpiryStatus(
                    url.expires_at
                )}

            </td>


            <td>

                <button
                    class="delete-btn"
                    onclick="deleteURL(
                        '${url.short_code}'
                    )">

                    🗑️ Delete

                </button>

            </td>

        `;


        tableBody.appendChild(row);

    });

}


/* ========================= */
/* DELETE URL */
/* ========================= */

async function deleteURL(shortCode) {

    const confirmDelete =
        confirm(
            "Are you sure you want to delete this URL?"
        );


    if (!confirmDelete) {

        return;

    }


    try {

        const response =
            await fetch(
                `/delete/${shortCode}`,
                {
                    method: "DELETE"
                }
            );


        const data =
            await response.json();


        if (!response.ok) {

            alert(
                data.error ||
                "Unable to delete URL."
            );

            return;

        }


        alert(
            "URL deleted successfully!"
        );


        // Refresh dashboard

        loadURLs();

    }


    catch (error) {

        console.error(error);


        alert(
            "Unable to connect to the server."
        );

    }

}


/* ========================= */
/* SEARCH URLS */
/* ========================= */

function searchURLs() {

    const searchInput =
        document.getElementById(
            "searchInput"
        );


    const searchText =
        searchInput.value
            .toLowerCase()
            .trim();


    // Empty search

    if (!searchText) {

        displayURLs(allURLs);

        return;

    }


    // Filter URLs

    const filteredURLs =
        allURLs.filter(function(url) {

            return (

                url.short_code
                    .toLowerCase()
                    .includes(searchText)

                ||

                url.original_url
                    .toLowerCase()
                    .includes(searchText)

            );

        });


    displayURLs(filteredURLs);

}


/* ========================= */
/* UPDATE ANALYTICS */
/* ========================= */

function updateAnalytics(urls) {

    // Total URLs

    const total =
        urls.length;


    // Total clicks

    const clicks =
        urls.reduce(function(total, url) {

            return total +
                Number(url.clicks || 0);

        }, 0);


    // Current time

    const now =
        new Date();


    let active = 0;

    let expired = 0;


    // Check URL status

    urls.forEach(function(url) {

        // URL without expiration

        if (!url.expires_at) {

            active++;

            return;

        }


        const expirationDate =
            new Date(url.expires_at);


        if (expirationDate > now) {

            active++;

        }
        else {

            expired++;

        }

    });


    // Update cards

    document.getElementById(
        "totalURLs"
    ).textContent = total;


    document.getElementById(
        "totalClicks"
    ).textContent = clicks;


    document.getElementById(
        "activeURLs"
    ).textContent = active;


    document.getElementById(
        "expiredURLs"
    ).textContent = expired;

}


/* ========================= */
/* EXPIRY STATUS */
/* ========================= */

function getExpiryStatus(expiresAt) {

    // URL never expires

    if (!expiresAt) {

        return `
            <span class="active-status">
                🟢 Never expires
            </span>
        `;

    }


    const expirationDate =
        new Date(expiresAt);


    const now =
        new Date();


    // URL expired

    if (expirationDate <= now) {

        return `
            <span class="expired-status">
                🔴 Expired
            </span>
        `;

    }


    // URL is active

    return `
        <span class="active-status">
            🟢 ${formatDate(expiresAt)}
        </span>
    `;

}


/* ========================= */
/* TRUNCATE LONG URL */
/* ========================= */

function truncateURL(url) {

    if (!url) {

        return "N/A";

    }


    if (url.length <= 40) {

        return url;

    }


    return url.substring(0, 40) + "...";

}


/* ========================= */
/* FORMAT DATE */
/* ========================= */

function formatDate(date) {

    if (!date) {

        return "Never";

    }


    return new Date(date)
        .toLocaleString();

}


/* ========================= */
/* LOAD DASHBOARD */
/* ========================= */

document.addEventListener(
    "DOMContentLoaded",
    loadURLs
);


/* ========================= */
/* ENTER KEY SUPPORT */
/* ========================= */

document
    .getElementById("urlInput")
    .addEventListener(
        "keydown",
        function(event) {

            if (event.key === "Enter") {

                shortenURL();

            }

        }
    );