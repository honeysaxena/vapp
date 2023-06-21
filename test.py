from videoapp.database import SessionLocal, Base
#from videoapp.playlists.models import Playlists
from videoapp.videos.models import Video



session = SessionLocal()

#obj = Playlists(title='Hello World')
#session.add(obj)
#session.commit()
#session.refresh(obj)

q = list(session.query(Video).limit(5).all()) #.values_list('host_id', flat=True)
host_ids = []
for val in q:
    val = val.host_id
    host_ids.append(val)
print(host_ids)
session.close()

#print(obj.db_id, obj.path)


