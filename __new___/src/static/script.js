function updateTime() {
    var now = new Date();
    
    var options = {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        hour12: false
    };
    
    var istTime = now.toLocaleString('en-US', { timeZone: 'Asia/Kolkata', ...options });
    var utcTime = now.toISOString().slice(0, 19).replace('T', ' ');

    document.getElementById('ist-time').textContent = istTime;
    document.getElementById('utc-time').textContent = utcTime;
}

setInterval(updateTime, 1000);