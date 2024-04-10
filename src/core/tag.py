from typing import List

from models.article import ArticleModel
from odmantic import AIOEngine


async def get_all_tags(engine: AIOEngine) -> List[str]:
    pipeline = [
        {
            "$unwind": {
                "path": "$tag_list",
                "preserveNullAndEmptyArrays": True,
            }
        },
        {
            "$group": {
                "_id": "all",
                "all_tags": {"$addToSet": "$tag_list"},
            }
        },
    ]
    col = engine.get_collection(ArticleModel)
    result = await col.aggregate(pipeline).to_list(length=1)
    if len(result) > 0:
        tags: List[str] = result[0]["all_tags"]
    else:
        tags = []
    return tags
