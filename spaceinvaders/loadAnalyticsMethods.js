const sendScore = (money, kills, time) => {
    console.log(`Sending score: ${money}, ${kills}, ${time}`);
    const token = window.token;

    if (!token) {
        console.error('No token set');
        return;
    }

    const data = {
        money,
        kills,
        time
    };

    const url = `${window.config.analytics_url}/game`;

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Failed to send score');
        }
        console.log('Score sent successfully');
    })
    .catch(error => {
        console.error('Error sending score:', error);
    });
};

console.log('Loaded analytics methods');

window.sendScore = sendScore;