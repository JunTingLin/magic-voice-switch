document.addEventListener('DOMContentLoaded', function() {
    setInterval(checkState, 3000); 
});

function checkState() {
    fetch('/api/state')
        .then(response => response.json())
        .then(data => {
            let content = document.getElementById('content');
            
            if (data.state === 1) {
                document.getElementById('theme-style').href = '/static/appearance/dark.css';
                content.textContent = '一片黑漆漆:( M3';
            } else if (data.state === 2) {
                document.getElementById('theme-style').href = '/static/appearance/lit.css';
                content.textContent = 'Damnnn超亮!'; 
            }
        })
}