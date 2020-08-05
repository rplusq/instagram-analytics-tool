import re
import requests
import dateutil.parser as dt
from PIL import Image
from io import BytesIO

# Function that pulls the hashtags from a caption
def get_hashtags(caption):
    caption = caption.lower()
    hashtag_pattern = re.compile(r"#\w+")
    res = re.findall(hashtag_pattern,caption)
    hashtags = list(map(lambda ht: ht[1:].lower(), res))
    return hashtags

# Function that allows to show the info from the iterrow of the Posts Data Frame
def display_post_info(iterrow):
    # Data parsing for print
    caption = iterrow[1][0]
    url = iterrow[1][1]
    timestamp = iterrow[1][5]
    likes = iterrow[1][6]
    comments = iterrow[1][7]
    engagement = iterrow[1][8]
    impressions = iterrow[1][9]
    reach = iterrow[1][10]
    saved = iterrow[1][11]
    video_views = iterrow[1][-1]
    date = dt.parse(timestamp)
    # Data parsing for img display
    media_type = iterrow[1][1]
    media_url = iterrow[1][2]
    thumbnail_url = iterrow[1][4]
    img_url = thumbnail_url if media_type == 'VIDEO' else media_url
    # We get the img from the url
    response = requests.get(img_url)
    img = Image.open(BytesIO(response.content))
    # We resize it
    resize_ratio = 0.25 if media_type == 'VIDEO' else 0.1675
    resized_img = img.resize((round(img.size[0]*resize_ratio), round(img.size[1]*resize_ratio)))
    # We display it
    display(resized_img)
    # Printing data
    print(f"Likes: {likes}.\nComments: {comments}.\nVideo Views: {video_views}.\nSaved: {saved}.")
    print(f"Engagement: {engagement}.\nImpressions: {impressions}.\nReach: {reach}.")
    print(f"Caption: {caption[:95]}...")
    print(f"Date: {date.day}/{date.month}/{date.year}")
    print(f"URL: {url}")

# Function that merges official post with unofficial API to get likes and comments
def merge_apis_data(official_posts, unofficial_posts):
    # Function that will merge the info from the Graph API and the Unofficial API
    def map_apis_info(official_post):
        new_post = official_post.copy()
        corresponding_post = next(filter(lambda unofficial_post: f"{unofficial_post['link']}/"  == official_post['permalink'],unofficial_posts), None)
        if corresponding_post is not None:
            new_post['likes'] = corresponding_post['likes_count']
            new_post['comments'] = corresponding_post['comments_count']
        return new_post
    return list(map(map_apis_info, official_posts))