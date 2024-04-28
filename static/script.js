document.addEventListener('DOMContentLoaded', function() {
    const apiKey = '809c51e1dc7f4b18aa46e2b4c4c6392c';
    const apiUrl = `https://newsapi.org/v2/top-headlines?q=health&apiKey=${apiKey}`;

    fetch(apiUrl)
    .then(response => response.json())
    .then(data => {
        const widgetBody = document.getElementById('widget-body');
        widgetBody.innerHTML = '';

        if (data.articles.length > 0) {
            const topArticles = data.articles.slice(0, 3);
            topArticles.forEach(article => {
                const articleTitle = article.title;
                const articleDate = new Date(article.publishedAt).toLocaleDateString();
                const articleLink = article.url;
                widgetBody.innerHTML += `
                    <div class="immunization-item">
                        <a href="${articleLink}" target="_blank">${articleTitle}</a> - ${articleDate}
                    </div>
                `;
            });
        } else {
            widgetBody.innerHTML = 'No recent health news found.';
        }
    })
    .catch(error => {
        console.error('Error:', error);
        const widgetBody = document.getElementById('widget-body');
        widgetBody.innerHTML = 'Error fetching health news.';
    });
});

function searchAndHighlight() {
    var searchText = document.getElementById("search-input").value;
    var content = document.getElementById("container").innerHTML;
    var highlightedContent = content.replace(new RegExp(searchText, "gi"), function(match) {
      return "<span style='background-color: yellow;'>" + match + "</span>";
    });
    document.getElementById("content").innerHTML = highlightedContent;}

const dashboard = document.getElementById('dashboard');

function subscribe(){
    var email = document.getElementById('email').value;
    if (email.trim() === "") {
        alert("Please enter a valid email address.");
        return false;
      }
    alert('Subscribed successfully!');
}
function toggleAnswer(button) {
    var answer = button.nextElementSibling;
    answer.style.display = answer.style.display === 'block' ? 'none' : 'block';
}


