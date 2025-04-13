from googleapiclient.discovery import build
import pandas as pd
import os

# User Input for API Key
api_key = input("Please enter your YouTube API key: ").strip()

# Playlist IDs (Modify this as needed); after list= in the URL
playlist_ids = ['PL4wA2s4MZ8hMYHC-khM7rsVbtauZIdjo3']

# Build the YouTube client
youtube = build('youtube', 'v3', developerKey=api_key)

# Function to get all video IDs from the playlist
def get_all_video_ids_from_playlists(youtube, playlist_ids):
    all_videos = []  # Initialize a single list to hold all video IDs

    for playlist_id in playlist_ids:
        next_page_token = None

        while True:
            try:
                playlist_request = youtube.playlistItems().list(
                    part='contentDetails',
                    playlistId=playlist_id,
                    maxResults=50,
                    pageToken=next_page_token
                )
                playlist_response = playlist_request.execute()

                all_videos += [item['contentDetails']['videoId'] for item in playlist_response.get('items', [])]

                next_page_token = playlist_response.get('nextPageToken')
                if not next_page_token:
                    break
            except Exception as e:
                print(f"Error retrieving videos for playlist {playlist_id}: {e}")
                break

    return all_videos

# Fetch all video IDs from the specified playlists
video_ids = get_all_video_ids_from_playlists(youtube, playlist_ids)

# Function to get replies for a specific comment
def get_replies(youtube, parent_id, video_id):
    replies = []
    next_page_token = None
    video_link = f"https://www.youtube.com/watch?v={video_id}"  # Generate video link

    while True:
        try:
            reply_request = youtube.comments().list(
                part="snippet",
                parentId=parent_id,
                textFormat="plainText",
                maxResults=100,
                pageToken=next_page_token
            )
            reply_response = reply_request.execute()

            for item in reply_response.get('items', []):
                comment = item['snippet']
                replies.append({
                    'Timestamp': comment['publishedAt'],
                    'Username': comment['authorDisplayName'],
                    'VideoID': video_id,
                    'VideoLink': video_link,  # Added video link column
                    'Comment': comment['textDisplay'],
                    'Date': comment.get('updatedAt', comment['publishedAt'])
                })

            next_page_token = reply_response.get('nextPageToken')
            if not next_page_token:
                break
        except Exception as e:
            print(f"Error retrieving replies for comment {parent_id}: {e}")
            break

    return replies

# Function to get all comments (including replies) for a single video
def get_comments_for_video(youtube, video_id):
    all_comments = []
    next_page_token = None
    video_link = f"https://www.youtube.com/watch?v={video_id}"  # Generate video link

    while True:
        try:
            comment_request = youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                pageToken=next_page_token,
                textFormat="plainText",
                maxResults=100
            )
            comment_response = comment_request.execute()

            for item in comment_response.get('items', []):
                top_comment = item['snippet']['topLevelComment']['snippet']
                all_comments.append({
                    'Timestamp': top_comment['publishedAt'],
                    'Username': top_comment['authorDisplayName'],
                    'VideoID': video_id,
                    'VideoLink': video_link,  # Added video link column
                    'Comment': top_comment['textDisplay'],
                    'Date': top_comment.get('updatedAt', top_comment['publishedAt'])
                })

                # Fetch replies if there are any
                if item['snippet']['totalReplyCount'] > 0:
                    all_comments.extend(get_replies(youtube, item['snippet']['topLevelComment']['id'], video_id))

            next_page_token = comment_response.get('nextPageToken')
            if not next_page_token:
                break
        except Exception as e:
            print(f"Error retrieving comments for video {video_id}: {e}")
            break

    return all_comments

# List to hold all comments from all videos
all_comments = []

# Fetch comments for each video
for video_id in video_ids:
    print(f"Fetching comments for video: {video_id}")
    video_comments = get_comments_for_video(youtube, video_id)
    all_comments.extend(video_comments)

# Create DataFrame
comments_df = pd.DataFrame(all_comments)

# Output to CSV
csv_file = 'comments_data.csv'
comments_df.to_csv(csv_file, index=False)

print(f"Comments saved to {csv_file}")
