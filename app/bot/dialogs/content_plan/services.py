from typing import Any
from app.bot.utils.schemas import PostData
from app.bot.db.models.schedule_post import SchedulePost

from datetime import timedelta, timezone, datetime, date

def parse_post_data(data: list[SchedulePost]) -> list[dict[str, Any]]:
    posts = []
    for post in data:
        posts.append(
            PostData(
                text=post.post_message,
                schedule_id=post.schedule_id,
                scheduled_time=post.scheduled_time,
                keyboard=post.data_json.get("keyboard"),
                has_spoiler=post.data_json.get("has_spoiler"),
                disable_notification=post.data_json.get("disable_notification"),
                file_id=post.data_json.get("file_id"),
            ).data_python
        )
    return posts


def find_selected_posts(posts: list[PostData], selected_date: datetime, tz_offset: int = None):
    result = []
    for post in posts:
        post.scheduled_time = post.scheduled_time.replace(
            tzinfo=timezone(offset=timedelta(hours=tz_offset))
        )
        
        if post.scheduled_time.date() == selected_date.date():
            result.append(post)
    return result

def get_dates_with_posts(posts: list[PostData]) -> set[str]:
    return {post.scheduled_time.date() for post in posts}