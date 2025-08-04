document.addEventListener('DOMContentLoaded', () => {
    updateAuthButton();
    const loginForm = document.getElementById('login-form');
    const placeDetailsSection = document.getElementById('place-details');
    const addReviewSection = document.getElementById('add-review');
    const token = getCookie('token');
    console.log('Current cookies:', document.cookie);
    console.log('Token found in cookie:', token);
    
    // Only run on place.html
    if (placeDetailsSection) {
        const placeId = getPlaceIdFromURL();

        if (!placeId) {
            placeDetailsSection.textContent = 'Place ID not found in URL.';
            return;
        }

        if (token) {
            addReviewSection.style.display = 'block';
            fetchPlaceDetails(token, placeId);
        } else {
            addReviewSection.style.display = 'none';
            fetchPlaceDetails(null, placeId);  // Public info still accessible
        }
        fetchReviewsByPlace(placeId);
    }

    // LOGIN LOGIC
    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;

            try {
                const response = await fetch('http://localhost:5000/api/v1/auth/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ email, password })
                });

                if (response.ok) {
                    const data = await response.json();
                    document.cookie = `token=${data.access_token}; path=/`;
                    window.location.href = 'index.html';
                } else {
                    const err = await response.json();
                    alert('Login failed: ' + (err.message || response.statusText));
                }
            } catch (error) {
                alert('Login failed: ' + error.message);
            }
        });
    }

    // PLACE LIST LOGIC (index.html only)
    const placesList = document.getElementById('places-list');
    const loginLink = document.getElementById('login-link');
    const priceFilter = document.getElementById('price-filter');

    if (placesList) {
        if (token) {
            fetchPlaces(token);
        }


        // Add filter options
        ['10', '50', '100', 'All'].forEach(value => {
            const option = document.createElement('option');
            option.value = value;
            option.textContent = value;
            priceFilter.appendChild(option);
        });

        priceFilter.addEventListener('change', () => {
            filterPlaces(priceFilter.value);
        });
    }

    const reviewForm = document.getElementById('review-form');

    if (reviewForm) {
        reviewForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            const token = getCookie('token');
            const placeId = getPlaceIdFromURL();
            const reviewText = document.getElementById('review_text').value.trim();

            if (!token || !placeId || !reviewText) {
                alert('You must be logged in and write a review.');
                return;
            }

            try {
                const review = await submitReview(token, placeId, reviewText);
                alert('Review submitted!');
                // Optionally refresh place details to show the new review
                fetchPlaceDetails(token, placeId);
                reviewForm.reset();
            } catch (err) {
                alert('Error submitting review: ' + err.message);
            }
        });
    }


    const createPlaceForm = document.getElementById('create-place-form');

    if (createPlaceForm) {
        const token = checkAuthentication();

        createPlaceForm.addEventListener('submit', async (event) => {
        event.preventDefault();

        const title = document.getElementById('title').value.trim();
        const description = document.getElementById('description').value.trim();
        const price = parseFloat(document.getElementById('price').value);
        const latitude = parseFloat(document.getElementById('latitude').value);
        const longitude = parseFloat(document.getElementById('longitude').value);

        try {
        const response = await fetch('http://localhost:5000/api/v1/places/', {
            method: 'POST',
            headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({
            title,
            description,
            price,
            latitude,
            longitude
            })
        });

        if (response.ok) {
            const data = await response.json();
            alert('Place created successfully!');
            window.location.href = `place.html?id=${data.id}`;
        } else {
            const error = await response.json();
            alert('Error: ' + (error.message || response.statusText));
        }

        } catch (err) {
        alert('Error submitting place: ' + err.message);
        }
    });
    }


    if (token && loginLink) {
        const nav = loginLink.parentElement;

        // Remove the login link (will replace it)
        loginLink.remove();

        // Create "Register Place" link
        const registerLink = document.createElement('a');
        registerLink.href = 'create_place.html';
        registerLink.className = 'login-button';
        registerLink.textContent = 'Register Place';

        // Create "Logout" link
        const logoutLink = document.createElement('a');
        logoutLink.href = '#';
        logoutLink.className = 'login-button';
        logoutLink.textContent = 'Logout';
        logoutLink.addEventListener('click', (e) => {
            e.preventDefault();
            document.cookie = 'token=; Max-Age=0; path=/';
            window.location.reload();
        });

        // Add both links to nav
        nav.appendChild(registerLink);
        nav.appendChild(logoutLink);
    }

});

// Get cookie value by name
function getCookie(name) {
    const cookies = document.cookie.split(';');
    for (const cookie of cookies) {
        const [key, val] = cookie.trim().split('=');
        if (key === name) return val;
    }
    return null;
}

// Fetch places from API and display them
async function fetchPlaces(token) {
    try {
        const response = await fetch('http://localhost:5000/api/v1/places/', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        if (response.ok) {
            const places = await response.json();
            console.log('Places data received:', places);
            displayPlaces(places);
        } else {
            console.error('Failed to fetch places:', response.statusText);
            const err = await response.text();
            console.error('Response body:', err);
        }

    } catch (err) {
        console.error('Error fetching places:', err);
    }
}

// Render places in the DOM
function displayPlaces(places) {
    const placesList = document.getElementById('places-list');
    if (!placesList) return;

    placesList.innerHTML = '';

    places.forEach(place => {
        const article = document.createElement('article');
        article.className = 'place-card';
        article.dataset.price = place.price;

        article.innerHTML = `
        <h3>${place.title}</h3>
        <p><strong>Price:</strong> $${place.price}/night</p>
        <p><strong>Location:</strong> (${place.latitude}, ${place.longitude})</p>
        <button class="details-button" onclick="location.href='place.html?id=${place.id}'">View Details</button>
        `;

        placesList.appendChild(article);
    });

    
}

// Filter displayed places by price
function filterPlaces(maxPrice) {
    const cards = document.querySelectorAll('.place-card');

    cards.forEach(card => {
        const price = parseFloat(card.dataset.price);
        if (maxPrice === 'All' || price <= parseFloat(maxPrice)) {
            card.style.display = 'block';
        } else {
            card.style.display = 'none';
        }
    });
}

function getPlaceIdFromURL() {
    const params = new URLSearchParams(window.location.search);
    return params.get('id');
}

async function fetchPlaceDetails(token, placeId) {
    try {
        const response = await fetch(`http://localhost:5000/api/v1/places/${placeId}`, {
            headers: token ? { 'Authorization': `Bearer ${token}` } : {}
        });

        if (!response.ok) throw new Error(`Failed to fetch place details (${response.status})`);

        const place = await response.json();
        displayPlaceDetails(place);
    } catch (err) {
        console.error('Error fetching place details:', err);
        document.getElementById('place-details').textContent = 'Could not load place details.';
    }
}

function displayPlaceDetails(place) {
    const section = document.getElementById('place-details');
    section.innerHTML = '';

    const wrapper = document.createElement('div');
    wrapper.className = 'place-details';

    const title = document.createElement('h2');
    title.textContent = place.title;

    const host = document.createElement('p');
    host.innerHTML = `<strong>Host:</strong> ${place.owner ? place.owner.first_name + ' ' + place.owner.last_name : 'Unknown'}`;

    const price = document.createElement('p');
    price.innerHTML = `<strong>Price:</strong> $${place.price}/night`;

    const desc = document.createElement('p');
    desc.innerHTML = `<strong>Description:</strong> ${place.description || 'N/A'}`;

    const location = document.createElement('p');
    location.innerHTML = `<strong>Location:</strong> ${place.latitude}, ${place.longitude}`;

    const amenities = document.createElement('p');
    const amenityList = (place.amenities || []).map(a => a.name).join(', ') || 'None';
    amenities.innerHTML = `<strong>Amenities:</strong> ${amenityList}`;

    
    wrapper.appendChild(title);
    wrapper.appendChild(host);
    wrapper.appendChild(price);
    wrapper.appendChild(desc);
    wrapper.appendChild(amenities);
    wrapper.appendChild(location);

    section.appendChild(wrapper);
}


function displayReviews(reviews) {
  const ul = document.getElementById('review-list');
  ul.innerHTML = '';

  reviews.forEach(r => {
    const li = document.createElement('li');
    li.classList.add('review-card');
    const rating = parseInt(r.rating || r.stars || 0);
    const fullStars = '★'.repeat(rating);
    const emptyStars = '☆'.repeat(5 - rating);

    li.innerHTML = `
      <p><strong>${r.user_name}:</strong></p>
      <p>${r.text}</p>
      <p><span class="rating-label">Rating:</span><span class="stars">${fullStars}${emptyStars}</span></p>
    `;

    ul.appendChild(li);
  });
}

function updateAuthButton() {
    const token = getCookie('token');
    const loginLink = document.getElementById('login-link');

    if (!loginLink) return;

    if (token) {
        loginLink.textContent = 'Logout';
        loginLink.href = '#';
        loginLink.addEventListener('click', (e) => {
            e.preventDefault();
            document.cookie = 'token=; Max-Age=0; path=/';
            window.location.reload();
        });
    } else {
        loginLink.textContent = 'Login';
        loginLink.href = 'login.html';
    }
}

function checkAuthentication() {
    const token = getCookie('token');
    if (!token) {
        window.location.href = 'index.html';
    }
    return token;
}

async function submitReview(token, placeId, reviewText) {
    try {
        const ratingInput = document.getElementById('rating');
        const ratingValue = parseInt(ratingInput.value);

        const response = await fetch(`http://localhost:5000/api/v1/reviews/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({
                text: reviewText,
                rating: ratingValue,
                place_id: placeId
            })
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Failed to submit review');
        }

        return await response.json();
    } catch (error) {
        throw error;
    }
}

async function fetchReviewsByPlace(placeId) {
    try {
        const response = await fetch(`http://localhost:5000/api/v1/places/${placeId}/reviews`);

        if (!response.ok) {
            throw new Error(`Failed to fetch reviews (${response.status})`);
        }

        const reviews = await response.json();
        displayReviews(reviews);
    } catch (err) {
        console.error('Error fetching reviews:', err);
        document.getElementById('reviews').innerHTML += '<p>Could not load reviews.</p>';
    }
}
