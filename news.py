from newsapi import NewsApiClient
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc


def get_latest_news():
    newsapi = NewsApiClient(api_key="c068324881794ed7be9bf778cf7c76cd")

    top_headlines = newsapi.get_everything(
        q="Arsenal OR Liverpool OR Chelsea OR Manchester OR Tottenham",
        sources="four-four-two, bbc-sport",
        language="en",
    )

    articles = top_headlines["articles"]

    # print(len(articles))

    # for article in articles:
    #     print(article["title"])
    #     print(article["author"])
    #     print(article["description"])
    #     print(article["url"])

    return articles


def generate_news_card(article):
    """ generate card for each news article, including title, description, content and a button for url"""
    title = article["title"]
    # description = article["description"]
    url = article["url"]
    content = article["content"]
    image = article["urlToImage"]

    card = dbc.Card(
        [
            # dbc.CardHeader(title),
            dbc.CardBody(
                children=[
                    html.H4(title, className="card-title"),
                    html.P(content, className="card-text"),
                    dbc.CardLink("Read More", href=url),
                    dbc.CardImg(src=image, title=title),
                ]
            ),
        ],
        className="mb-3",
    )

    return card


def main():
    get_latest_news()


if __name__ == "__main__":
    main()

# url = (
#     "http://newsapi.org/v2/everything?"
#     "q=premier&"
#     "from=2020-09-03&"
#     "sortBy=popularity&"
#     "apiKey=c068324881794ed7be9bf778cf7c76cd"
# )
# response = requests.get(url)
# print(response.json())
