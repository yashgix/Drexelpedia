function ArticleListViewer(articleSource) {
    const ARTICLES_PER_PAGE = 10;

    this.load = function() {
        this.articles = $.get(`/api/${articleSource}`, function(data, status) {
            if (status !== "success") {
                alert("Could not fetch recent articles. Status: " + status);
                return;
            }
            for (let article of data) {
                const modificationTime = new Date(article.last_modification_time).toLocaleString();
                $(".article-list").append($("<div class='article-card-shadow'></div>").append(
                    $("<div class='article-card article-card-abbreviated'></div>")
                        .append($(`<h2>${article.title}</h2>`))
                        .append($(
                            "<p class='modification-info'>" +
                            `<i>Last modified by ${article.last_modifier_username} on ${modificationTime}</i>` + 
                            `<span style='float: right;'><strong>${article.votes}</strong> votes</span></p>`
                        ))
                        .append($(`<div>${article.content}</div>`))
                        .append($("<p class='read-more'></p>"))
                        .click(function() {
                            window.location.href = `/article/${article.id}`;
                        })
                ));
            }
        });
    };
}
