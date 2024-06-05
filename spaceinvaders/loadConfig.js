fetch('/config.json')
    .then(response => response.json())
    .then(data => {
        window.config = data;
    })
    .catch(error => console.error('Error:', error));