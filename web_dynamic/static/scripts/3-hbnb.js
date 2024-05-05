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

  $.post('http://localhost:5001/api/v1/places_search/', '{}', function (data, status) {
    data.forEach(function (place) {
      const article = $('<article></article>');
      const title = $('<div class="title"></div>').append('<h2>' + place.name + '</h2>');
      const price = $('<div class="price_by_night"></div>').text('$' + place.price_by_night);
      const info = $('<div class="information"></div>').append('<div class="max_guest">' + place.max_guest + ' Guest' + (place.max_guest !== 1 ? 's' : '') + '</div>').append('<div class="number_rooms">' + place.number_rooms + ' Bedroom' + (place.number_rooms !== 1 ? 's' : '') + '</div>').append('<div class="number_bathrooms">' + place.number_bathrooms + ' Bathroom' + (place.number_bathrooms !== 1 ? 's' : '') + '</div>');
      const description = $('<div class="description"></div>').text(place.description);
      article.append(title).append(price).append(info).append(description);
      $('section.places').append(article);
    });
  });
});
  