from videoapp.database import SessionLocal, Base
#from videoapp.playlists.models import Playlists
from videoapp.videos.models import Video
from videoapp.users.models import User
from videoapp.videos.extractors import extract_video_id
from videoapp.playlists.models import Playlists

session = SessionLocal()

user1 = session.query(User).filter_by(email='xyz@gmail.com').one()
print(user1)


url1 = "https://youtu.be/WIoyIYgghcI"
#url2 = "https://www.youtube.com/watch?v=8NaHaRS0_DA"
#host_id = extract_video_id(url2)

obj_2, created = Video.get_or_create(url1, user_id=user1.user_id)

session.close()
print(obj_2, created)

'''
url = "https://www.youtube.com/watch?v=WIoyIYgghcI&t=618s"

host_id = extract_video_id(url)
obj = session.query(Video).filter_by(host_id=host_id).one()
session.close()
print(obj)
'''


#obj = Playlists(title='Hello World')
#session.add(obj)
#session.commit()
#session.refresh(obj)

#q = list(session.query(Video).limit(5).all()) #.values_list('host_id', flat=True)
#host_ids = []
#for val in q:
#    val = val.host_id
#    host_ids.append(val)
#print(host_ids)
#session.close()

#print(obj.db_id, obj.path)


