function initialize() {
    var mapOptions = {
        center: new google.maps.LatLng(35.045738,-85.309525),
        zoom: 14,
        mapTypeId: google.maps.MapTypeId.ROADMAP
    };

    tw.map = new google.maps.Map(document.getElementById("map"), mapOptions);
    tw.set_slider($('#slider'));
    tw.move_slider_to_now();
    tw.get_categories();
    tw.get_events();

}

// slider
$(function(){

    // Slider
    $('#slider').slider({
        value: 50
    });

    //hover states on the static widgets
    $('#dialog_link, ul#icons li').hover(
        function() { $(this).addClass('ui-state-hover'); },
        function() { $(this).removeClass('ui-state-hover'); }
    );

});

// main Tentwork object
var TW = {
    dummy_data: JSON.parse('{"data": [{"category": {"link": "https://tentwatch.com/categories/3", "name": "Stalled Car", "parent": {"link": "https://tentwatch.com/parent-categories/4", "name": "Traffic"}}, "id": 3, "link": "https://tentwatch.com/events/3", "location": {"lat": 35.045738, "long": -85.309525}, "created": "2012-09-15T06:13:30Z"}, {"category": {"link": "https://tentwatch.com/categories/1", "name": "Shooting", "parent": {"link": "https://tentwatch.com/parent-categories/1", "name": "Criminal Activity"}}, "id": 2, "link": "https://tentwatch.com/events/2", "location": {"lat": 35.035738, "long": -85.299525}, "created": "2012-09-15T12:00:58Z"}, {"category": {"link": "https://tentwatch.com/categories/1", "name": "Shooting", "parent": {"link": "https://tentwatch.com/parent-categories/1", "name": "Criminal Activity"}}, "id": 1, "link": "https://tentwatch.com/events/1", "location": {"lat": 35.055738, "long": -85.319525}, "created": "2012-09-15T18:00:32Z"}]}'),

    // constants
    CATEGORIES_LIST_ID: '#categories',
    CIRCLE_MAX_OPACITY: 0.85,
    CIRCLE_FADE_THRESHOLD_SECONDS: 60*60,
    CIRCLE_FADE_LENGTH_SECONDS: 60*60,
    CIRCLE_OPTIONS: {
        center: null,
        strokeColor: "#FF0000",
        strokeOpacity: 0.0,
        strokeWeight: 0,
        fillColor: "#0eb3dc",
        fillOpacity: 0.65,
        map: null,
        radius: 200
    },

    events: [],
    map: null,
    slider: null,

    clear_all_circles: function() {
        while ( this.events.length > 0 ) {
            var event = this.events.pop();
            if (event.circle) {
                event.circle.setMap(null);
            }
        }
    },

    draw_event: function(event) {
        var options = this.CIRCLE_OPTIONS;
        options.center = new google.maps.LatLng(event.location.lat, event.location.long);
        options.map = this.map;
        console.log('options', options);
        var circle = new google.maps.Circle(options);

        return circle;
        
        // function resize(circle) {
        //     console.log('circle', circle.radius);
        //     if (circle.radius < 1000) {
        //         console.log('init', circle.radius);
        //         circle.radius = circle.radius + 10;
        //     } else {
        //         clearInterval(animate);
        //     }
        // }

        // var animate = setInterval(function() { resize(circle) },
        // 10);
    },

    filter_time: function(value) {
        // convert value (0..99) to seconds
        var slider_seconds = ((value+1) / 100) * (24*60*60);
        
        for (event in this.events) {
            var e = this.events[event];
            var event_seconds = e.created.getHours()*60*60 + e.created.getMinutes()*60 + e.created.getSeconds();

            if (slider_seconds >= event_seconds) {
                // show the circle
                if (e.circle.map == null) {
                    e.circle.setMap(this.map);
                }

                // // fade
                // if (slider_seconds - this.CIRCLE_FADE_THRESHOLD_SECONDS >= event_seconds) {
                //     e.circle.fillOpacity = 0.3;

                // } else {
                //     console.log('max op');
                //     e.circle.fillOpacity = this.CIRCLE_MAX_OPACITY;
                // }
            } else {
                e.circle.setMap(null);
            }
        }
    },

    get_categories: function() {
        var tw = this;
        $.getJSON('http://tentwatch.com/parent-categories/?format=json', function(data) {
            var $cat_list = $(tw.CATEGORIES_LIST_ID);
            $.each(data.data, function() {
                var parents = this;
                var $parent_menu_item = $('<li class="dropdown-submenu"><a tabindex="-1" href="#">' + parents.name + '</a></li>');
                
                var $submenu = $('<ul class="dropdown-menu"></ul>');
                // parent categories
                $.each(parents.children, function() {
                    $submenu.append('<li class="sub_menu_item" data-link="' + this.link + '" data-cat-name="' + parents.name + ' - ' + this.name + '" data-parent-cat="' + parents.name + '" data-cat="' + this.name + '"><a tabindex="-1" href="#">' + this.name + '</a></li>');
                });
                $parent_menu_item.append($submenu);
                $cat_list.append($parent_menu_item);
            });

            // show events for category on click
            $cat_list.on('click', '.sub_menu_item', function() {
                var cat_id = /(\d+)$/.exec($(this).attr('data-link'))[0];
                $('a.category-name').text($(this).attr('data-cat-name'));
                tw.clear_all_circles();
                tw.get_events($(this).attr('data-parent-cat'), $(this).attr('data-cat'));
            });
        });
    },

    get_events: function(parent, child) {
        var tw = this;
        var path;

        tw.clear_all_circles();
        if (!parent) {
            path = 'events?format=json';
        } else {
            path = 'events/?format=json&parent_category=' + encodeURIComponent(parent);

            if (child) {
                path += '&category=' + encodeURIComponent(child);
            }
        }
        $.getJSON('http://tentwatch.com/' + path, function(data) {
            if (data.data) {
                tw.load(data.data);
                tw.show_events();
            }
        });
    },

    load: function(events) {
        for (var event in events) {
            events[event].circle = null;

            // convert date string to object
            events[event].created = new Date(events[event].created);

            if (this.events === null) {
                this.events = [];
            }
            this.events.push(events[event]);
            
        }
    },

    // changes the position of the slider
    // value: integer 0 to 99
    move_slider: function(value) {
        this.slider.slider('value', value);
    },

    move_slider_to_now: function() {
        var MAX_SECONDS = 24 * 60 * 60;
        var now = new Date();
        var now_seconds = now.getHours()*60*60 + now.getMinutes()*60 + now.getSeconds();

        this.move_slider(100 * now_seconds/MAX_SECONDS);
    },

    set_slider: function(slider) {
        var tw = this;
        tw.slider = slider;
        
        $(this.slider).on('slide', function() {
            tw.filter_time($(this).slider('value'));
        });
    },

    show_events: function(events) {
        if (!events) { var events = this.events; }
        for (var event in events) {
            events[event].circle = this.draw_event(events[event]);
        }
    }
};

if (!window.tw) { window.tw = TW; }

$(document).ready(function() {
    initialize();

    $('.dropdown-toggle').dropdown();
});