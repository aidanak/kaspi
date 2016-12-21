
var Geocoder = {

    init: function (map) {
        this._map = map;
        this.bindElements();
        this.bindEvents();

        this.markerGroup = L.featureGroup().addTo(this._map);
    },

    bindEvents: function () {

        // Инициализируем плагин typeahead
        this.searchField.typeahead({
            minLength: 1,
            highlight: true
        }, {
            limit: 6,
            displayKey: 'name',
            // При каждом изменении input поля отправляем запрос
            source: this.sendRequest.bind(this),

            templates: {
                suggestion: this.renderTemplate.bind(this),
                notFound: function () {
                    return '<div class="tt-no-result">Нет результатов...</div>';
                }
            }
        });

        // Инициализируем событие клика на результат поиска
        this.searchField.bind('typeahead:select', this.onResultItemClick.bind(this));

    },

    bindElements: function () {
        this.searchField = $('.js-search');
    },

    sendRequest: function (q, sync, async) {
         $.ajax({
            type: 'GET',
            url: 'http://localhost:8000/api/search/',
            dataType: 'json',
            contentType: "application/json; charset=utf-8",
            data: {
                'text': q
            },
            success: function (response) {
                  var data = new Array();

                  var itemCollection =  response.addrs.features;

                  $.each(itemCollection, function(index, value){

                        var prop = value.properties;

                        var name =  prop.region + ', ' +
                                    prop.locality + ', ' +
                                    prop.street + ', ' +
                                    prop.house;

                        data.push({
                            coordinates: value.geometry.coordinates,
                            name: name
                        });

                    });

                async(data);
            }
        });
    },

     renderTemplate: function (data) {

        var suggestion = '<div class="list-item clearfix">' +
                          '<div class="list-item-r">' +
                            '<h4 class="list-item-name item-name" title="' + data.name + '">' + data.name +  '</h4>' +
                          '</div>' +
                        '</div>';

        return suggestion;
    },

    onResultItemClick: function(ev, suggestion){

        var coordinates = suggestion.coordinates;
        var marker = L.marker(coordinates);

        this.clearMap();
        this.markerGroup.addLayer(marker);
        this._map.setView(new L.LatLng(coordinates[0], coordinates[1]), 15)
    },

    clearMap: function () {
        this.markerGroup.clearLayers();
    }
};