$(document).ready(function () {
  const amenities = {};
  $('input[type="checkbox"]').change(function () {
    if ($(this).is(':checked')) {
      amenities[$(this).data('id')] = $(this).data('name');
    } else {
      delete amenities[$(this).data('id')];
    }
    const names = Object.values(amenities).join(', ');
    if (names.length > 0) {
      $('.amenities h4').text(names);
    } else {
      $('.amenities h4').html('&nbsp;');
    }
  });

  $.get('http://localhost:5001/api/v1/status/', function (data, status) {
    if (data.status === 'OK') {
      $('div#api_status').addClass('available');
    } else {
      $('div#api_status').removeClass('available');
    }
  });

  $.ajax({
    url: 'http://localhost:5001/api/v1/users/',
    type: 'GET',
    success: function (users) {
      const userData = {};
      users.forEach(function (user) {
        userData[user.id] = user;
      });

      $.ajax({
        url: 'http://localhost:5001/api/v1/places_search/',
        type: 'POST',
        data: JSON.stringify({ states: [], cities: [], amenities: [] }),
        contentType: 'application/json',
        success: function (data) {
          data.forEach(function (place) {
            const user = userData[place.user_id];
            const article = $('<article></article>');
            const title = $(`<h2>${place.name}</h2>`);
            const price = $(`<div class="price_by_night"><p>$${place.price_by_night}</p></div>`);
            const info = $('<div class="information"></div>')
              .append(`<div class="max_guest"><div class="guest_image"></div>${place.max_guest} Guest${place.max_guest !== 1 ? 's' : ''}</div>`)
              .append(`<div class="number_rooms"><div class="bed_image"></div>${place.number_rooms} Bedroom${place.number_rooms !== 1 ? 's' : ''}</div>`)
              .append(`<div class="number_bathrooms"><div class="bath_image"></div>${place.number_bathrooms} Bathroom${place.number_bathrooms !== 1 ? 's' : ''}</div>`);
            const users = $(`<div class="user"><p><b>Owner:</b> ${place.user_id ? `${user.first_name} ${user.last_name}` : 'Loading'}</p></div>`);
            const description = $(`<div class="description">${place.description}</div>`);
            article.append(title).append(price).append(info).append(users).append(description);
            $('section.places').append(article);
          });
        }
      });
    }
  });
});
