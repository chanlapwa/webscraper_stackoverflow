import requests
from bs4 import BeautifulSoup

url = 'https://stackoverflow.com/?tab=month'
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')

results = soup.find(id='question-mini-list')

post_list = []

post_elements = results.find_all('div', class_='s-post-summary js-post-summary')

for post_element in post_elements:
    title = post_element.find('a', class_='s-link')
    # since "votes", "answers" and "views" share the same class tag: "s-post-summary--stats-item-number", the scraper needs to fetch one level up first
    votes_element = post_element.find('div', class_='s-post-summary--stats-item s-post-summary--stats-item__emphasized')
    votes = votes_element.find('span', class_='s-post-summary--stats-item-number')
    # "answers" and "views" involve two possible class tags, thus use a lambda function here to include all possibilities
    func = lambda x, y : post_element.find('div', class_= x) if post_element.find('div', class_ = x) != None else post_element.find('div', class_= y)
    answers_element = func('s-post-summary--stats-item has-answers', 's-post-summary--stats-item has-answers has-accepted-answer')
    answers = answers_element.find('span', class_='s-post-summary--stats-item-number')
    views_element = func('s-post-summary--stats-item', 's-post-summary--stats-item is-hot')
    views = views_element.find('span', class_='s-post-summary--stats-item-number')

    post_list.append({'title': title.text, 'votes': votes.text, 'answers': answers.text, 'views': views.text})
    
print(post_list)

