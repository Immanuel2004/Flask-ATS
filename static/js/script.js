document.querySelector("#applicationForm").addEventListener("submit", function (e) {
    e.preventDefault();
    const formData = new FormData(this);

    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById('resultContainer').style.display = 'block';
        document.getElementById('suggestions').innerText = data.suggestions;

        if (data.matchScore !== undefined) {
            drawDonutChart(data.matchScore);
        } else {
            console.error("matchScore not found in response");
        }
    })
    .catch(err => {
        console.error("Error during submission:", err);
    });
});
