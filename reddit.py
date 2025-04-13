import praw
import csv

# Initialize the Reddit instance
reddit = praw.Reddit(
    client_id='ypXSFJSJ_QpONh4yCaSzKw',
    client_secret='80JuQPDLQPm8PVvWsU4zeMgfQ2XAJg',
    user_agent='No_Bullfrog8687'
)

def scrape_reddit_comments(url):
    submission = reddit.submission(url=url)
    submission.comments.replace_more(limit=None)
    comments = submission.comments.list()
    
    return comments

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
    
    def get_comment_hierarchy(comments):
        comment_dict = {}
        for comment in comments:
            comment_dict[comment.id] = {
                'body': comment.body,
                'author': str(comment.author),
                'score': comment.score,
                'created_utc': comment.created_utc,
                'parent_id': comment.parent_id.split('_')[1] if '_' in comment.parent_id else None
            }
        return comment_dict

    def export_to_csv_with_hierarchy(comment_dict, filename='reddit_comments_with_hierarchy.csv'):
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Comment ID', 'Comment Body', 'Author', 'Score', 'Created UTC', 'Parent Comment ID'])
            for comment_id, comment_data in comment_dict.items():
                writer.writerow([
                    comment_id,
                    comment_data['body'],
                    comment_data['author'],
                    comment_data['score'],
                    comment_data['created_utc'],
                    comment_data['parent_id']
                ])

    comment_dict = get_comment_hierarchy(comments)
    export_to_csv_with_hierarchy(comment_dict)