from algoliasearch.search_client import SearchClient
from videoapp.database import session
from videoapp.config import settings
from videoapp.videos.models import Video
from indexing.schemas import VideoIndexSchema

ALGOLIA_APP_ID=settings.algolia_app_id
ALGOLIA_API_KEY=settings.algolia_api_key
ALGOLIA_INDEX_NAME=settings.algolia_index_name

def get_index(name=ALGOLIA_INDEX_NAME):
    client = SearchClient.create(ALGOLIA_APP_ID, ALGOLIA_API_KEY)
    index = client.init_index(name)
    return index

def get_dataset():
    video_q = [x.__dict__ for x in session.query(Video).all()]
    videos_dataset = [VideoIndexSchema(**x).dict() for x in video_q]
    dataset = videos_dataset
    return dataset

def update_index():
    index = get_index()
    dataset = get_dataset()
    idx_resp = index.save_objects(dataset).wait()
    try:
        count = len(list(idx_resp[0]['objectIDs'])) 
    except:
        count = None
    return count

def search_index(query):
    index = get_index()
    return index.search(query)
