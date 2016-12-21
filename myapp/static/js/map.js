;(function () {

    var Map = {
        init: function () {

            // Инициализируем карту
            this.mapInit();

            // Инициализируем геокодер
            Geocoder.init(this.map);
        },

        mapInit: function () {

            // Создаем карту
            this.map = L.map('map').setView(['43.226957', '76.830795'], 12);

            // Создаем слой тайлов
            L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
                attribution: '&copy; <a href="http://openstreetmap.org/copyright">OpenStreetMap   contributors</a>',
                id: 'mapbox.streets'
            }).addTo(this.map);

        }
    };


    $(document).ready(function () {
        Map.init();
    });

}());