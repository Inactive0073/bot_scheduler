from app.bot.utils.schemas import PostData
from app.bot.db.models.schedule_post import SchedulePost

from datetime import timedelta, timezone, datetime

def parse_post_data(data: list[SchedulePost]) -> list[PostData]:
    posts = []
    for post in data:
        posts.append(PostData(
            text=post.post_message,
            scheduled_time=post.scheduled_time,
            keyboard=post.data_json.get("keyboard"),
            has_spoiler=post.data_json.get("has_spoiler"),
            disable_notification=post.data_json.get("disable_notification"),
            file_id=post.data_json.get("file_id"),
        ))
    return posts


def find_today_posts(posts: list[PostData], tz_offset: int = None):
    posts = []
    for post in posts:
        post.scheduled_time.tzinfo = timezone(offset=timedelta(hours=tz_offset)) 
        if post.scheduled_time.date() == datetime.now(timezone(offset=timedelta(hours=tz_offset))).date():
            posts.append(post)
    return posts
