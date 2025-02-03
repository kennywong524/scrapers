import praw
import csv

# Initialize the Reddit instance
reddit = praw.Reddit(
    client_id='YOUR_CLIENT_ID',
    client_secret='YOUR_CLIENT_SECRET',
    user_agent='YOUR_USER_AGENT'
)

def scrape_reddit_comments(url):
    submission = reddit.submission(url=url)
    submission.comments.replace_more(limit=None)
    comments = submission.comments.list()
    
    for comment in comments:
        print(comment.body)

if __name__ == "__main__":
    url = input("Enter the Reddit post URL: ")
    scrape_reddit_comments(url)
    def export_to_csv(comments, filename='reddit_comments.csv'):
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Comment ID', 'Comment Body', 'Author', 'Score', 'Created UTC'])
            for comment in comments:
                writer.writerow([comment.id, comment.body, str(comment.author), comment.score, comment.created_utc])

    if __name__ == "__main__":
        url = input("Enter the Reddit post URL: ")
        comments = scrape_reddit_comments(url)
        export_to_csv(comments)