$(function() {
    $('#map').css('height', $(window).height() - 80);
    var geocoder = function() {};

    geocoder.prototype = {
        init: function() {
            this.markers = [];
            this._map = L.map('map').setView(['43.226957', '76.830795'], 12);

            L.tileLayer('http://kaspi-city-tile1-p:80/osm_tiles/{z}/{x}/{y}.png', {
                attribution: '&copy; <a href="http://openstreetmap.org/copyright">OpenStreetMap   contributors</a>',
                id: 'mapbox.streets'
            }).addTo(this._map);
            // L.tileLayer('http://tile.openstreetmap.org/{z}/{x}/{y}.png', {
            //     maxZoom: 18,
            //     attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',

            // }).addTo(this._map);
            this.init_listeners();
        },
        add_marker: function(item){
               this.clear_map();
               var marker = L.marker(item.coordinates).addTo(this._map);
               
               this._map.setView(new L.LatLng(item.coordinates[0], item.coordinates[1]), 17)
        },
        clear_map: function() {
            for (var i = 0; i < this.markers.length; i++) {
                if (this.markers[i]) {
                    this.markers[i].closePopup();
                    this.markers[i].unbindPopup();
                    this._map.removeLayer(this.markers[i]);
                }
                delete this.markers[i];
            }
        },
        init_listeners: function() {
            var _this = this;
            $('.search-form').on('submit', function(e){
                e.preventDefault();
                var address = $('.search-form').val();
                $.ajax({
                    url: 'http://localhost:8000/api/search/?&text=' + address,
                    type: 'GET',
                    dataType: 'json',
                    contentType: 'application/json',
                    success: function(response) {
                        _this.add_marker(response.addrs.features[0].geometry);

                    }
                });
            })
        }
    };

    window.geocoder = new geocoder();
    window.geocoder.init();
});
