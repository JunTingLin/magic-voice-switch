$(document).ready(function() {
    setInterval(checkState, 1000);
});

function checkState() {
    $.getJSON('/api/state', function(data) {
        let $content = $('#content');
        
        if (data.state === 1) {
            $('#theme-style').attr('href', '/static/appearance/dark.css');
            $content.text('一片黑漆漆:( M3');
        } else if (data.state === 2) {
            $('#theme-style').attr('href', '/static/appearance/lit.css');
            $content.text('Damnnn超亮!');
        } else {
        }
        // TODO: Add more states
    });
}
