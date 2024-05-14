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
        document.getElementById('result').style.display = 'block';
        document.getElementById('deleteButton').style.display = 'inline-block';
    })
    .catch(error => console.error('Error:', error));
});

document.getElementById('deleteButton').addEventListener('click', function() {
    document.getElementById('result').innerHTML = '';
    document.getElementById('result').style.display = 'none';
    document.getElementById('deleteButton').style.display = 'none';
});