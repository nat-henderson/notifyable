$(document).ready(function() {
    var channel_container = $('#channel-container');

    // No need to parseJSON this; jQuery already takes care of this
    var endpoints = channel_container.data('channels') || {};
    var remaining = _.keys(endpoints).length;
    var isotope_elements = [];

    _.each(endpoints, function(endpoint) {
        $.getJSON(endpoint, function(data){
            var channel_div = $("<div class='channel' data-endpoint='" + endpoint + "'></div>");
            channel_div.css('background-color', data['color']);

            init_channel(channel_div, data);

            isotope_elements.push(channel_div);
            remaining -= 1;

            if (remaining === 0) {
                channel_container.empty();
                _.each(isotope_elements, function(element) {
                    element.appendTo(channel_container);
                });
                channel_container.isotope({
                    itemSelector: '.channel',
                    layoutMode: 'masonry'
                });
            }
        }).fail(function() {
            remaining -= 1;
        });
    });

    var refresh_endpoints = function() {
        _.each(channel_container.children(), function(element) {
            var endpoint = element.data('endpoint');
            $.getJSON(endpoint, function(data){
                var channel_div = $("<div class='channel'></div>");
                channel_div.css('background-color', data['color']);

                init_channel(channel_div, data);
                element.replaceWith(channel_div);
                channel_container.isotope('reLayout');
            });
        });
    };
    $('#refresh').click(refresh_endpoints);

    function init_channel(root, data) {
        root.css('background-color', data['color']);
        var content_div = $("<div class='channel-content'></div>");
        content_div.css('background-color', shadeColor(data['color'], 95));
        populate_content(content_div, data);
        content_div.appendTo(root);

        $("<h5 class='service-name'>" + data['channel'] + "</h5>").appendTo(root);
    }

    function populate_content(root, data) {
        var elements = [];
        if (data['title']) {
            elements.push("<h1 class='content-title'>" + data['title'] + "</h1>");
        }

        if (data['type'] === 'text') {
            elements.push("<p class='content-text'>" + data['text'] + "</p>");
            if (data['image']) {
                console.warn("Images are currently unsupported on 'text' posts");
            }
        } else if (data['type'] === 'image') {
            elements.push("<img class='content-image' src='" + data['image'] + "'>");

            var caption = data['text'];
            if (caption) {
                elements.push("<p class='content-caption'>" + caption + "</p>");
            }
        } else {
            console.warn("Unsupported data type " + data['type']);
        }

        var meta = data['meta'];
        if (meta) {
            elements.push(create_meta_div(meta));
        }

        $(elements.join('')).appendTo(root);
    }

    function create_meta_div(meta) {
        var text = meta['text'];
        var image = meta['image'];

        var html = "<div class='content-meta'>";
        if (image) {
            html += "<img src='" + image + "'>";
        }
        html += "<h4>" + text + "</h4>";
        html += "</div>";

        return html;
    }

    // http://stackoverflow.com/questions/5560248/programmatically-lighten-or-darken-a-hex-color
    function shadeColor(color, percent) {
        var num = parseInt(color.slice(1),16), amt = Math.round(2.55 * percent), R = (num >> 16) + amt, B = (num >> 8 & 0x00FF) + amt, G = (num & 0x0000FF) + amt;
        return "#" + (0x1000000 + (R<255?R<1?0:R:255)*0x10000 + (B<255?B<1?0:B:255)*0x100 + (G<255?G<1?0:G:255)).toString(16).slice(1);
    }
});