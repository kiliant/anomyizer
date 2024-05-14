document.getElementById('anonymizeForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const textInput = document.getElementById('textInput').value;
    fetch('/anonymize', {
        method: 'POST',
        headers: {
            'Content-Type': 'text/plain',
        },
        body: textInput,
    })
    .then(response => response.text())
    .then(data => {
        const formattedData = data.replace(/\n/g, '<br />')
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;");
        console.log(formattedData);
        document.getElementById('result').innerHTML = `Anonymisierter Text:<br />${formattedData}`;
    })
    .catch(error => console.error('Error:', error));
});