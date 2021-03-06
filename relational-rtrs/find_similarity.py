import sys
from models import Movie, Similarity, get_db

if len(sys.argv) != 2:
    print("Usage %s movie_id" % sys.argv[0])
    sys.exit(1)

movie_id = int(sys.argv[1])

db= get_db()
rec = db.query(Movie).filter_by(movie_id=movie_id).first()
print("Title: {}, Genres: {}".format(rec.title, rec.genres))

res=db.execute('select movie_id_1, movie_id_2, ((title_similarity_index * 1) + (genres_similarity_index * 0.6)) as overall_similarity from similarities where movie_id_1=%i or movie_id_2=%i order by overall_similarity desc limit 10' % (movie_id, movie_id))
#res=db.execute('select movie_id_1, movie_id_2, ((title_similarity_index * 1) + (genres_similarity_index * 0.6)) as overall_similarity from similarities where movie_id_1=%i or movie_id_2=%i order by ((title_similarity_index * 1) + (genres_similarity_index * 0.6)) limit 10' % (movie_id, movie_id))

i = 0
rec_count = 10      
for r in res:
    i += 1
    if(r[0]!= movie_id):
        m = db.query(Movie).filter_by(movie_id=r[0]).first()
    else:
        m = db.query(Movie).filter_by(movie_id=r[1]).first()

    print("Movie: %s - Genres: %s - Similarity: %f" % (m.title, m.genres, r[2]))
    
