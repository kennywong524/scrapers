import requests
from bs4 import BeautifulSoup

def scrape_forum(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    forum_data = []

    # Extract forum content
    forum_content_elem = soup.find('div', class_='message-content')
    forum_content = forum_content_elem.get_text(strip=True) if forum_content_elem else 'No forum content found'
    
    # Extract comments
    comments = soup.find_all('div', class_='message')
    for comment in comments:
        user = comment.find('a', class_='username').get_text(strip=True)
        content = comment.find('div', class_='message-content').get_text(strip=True)
        score = comment.find('span', class_='reaction-score').get_text(strip=True) if comment.find('span', class_='reaction-score') else '0'
        
        forum_data.append({
            'user': user,
            'content': content,
            'score': score
        })

    return forum_content, forum_data

if __name__ == "__main__":
    url = input("Enter the forum URL: ")
    forum_content, forum_data = scrape_forum(url)

    print("Forum Content:")
    print(forum_content)
    print("\nComments:")
    for data in forum_data:
        print(f"User: {data['user']}")
        print(f"Content: {data['content']}")
        print(f"Score: {data['score']}")
        print("-" * 20)


