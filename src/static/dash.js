$(document).ready(function() {
    var channel_container = $('#channel-container');
    var container_is_empty = true;
    channel_container.isotope({
        itemSelector: '.channel',
        layoutMode: 'fitRows'
    });

    // No need to parseJSON this; jQuery already takes care of this
    var endpoints = channel_container.data('channels');

    for (var channel in endpoints) {
        if (endpoints.hasOwnProperty(channel)) {
            var endpoint = endpoints[channel];

            $.getJSON(endpoint, function(data){
                if (container_is_empty) {
                    container_is_empty = false;

                    // Container contains Loading... text, so empty that
                    channel_container.empty();
                }
                var channel_div = $("<div class='channel'></div>");
                channel_div.css('background-color', data['color']);

                init_channel(channel_div, data);

                channel_div.appendTo(channel_container);
            });
        }
    }

    function init_channel(root, data) {
        root.css('background-color', data['color']);
        var content_div = $("<div class='channel-content'></div>");
        populate_content(content_div, data);
        content_div.appendTo(root);

        $("<h1 class='service-name'>" + data['channel'] + "</h1>").appendTo(root);
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
            elements.push("<p class='content-caption'>" + data['text'] + "</p>");
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
        html += "<h1>" + text + "</h1>";
        html += "</div>";

        return html;
    }
});