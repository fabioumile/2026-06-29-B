from database.DB_connect import DBConnect
from model.album import Album
from model.arco import Arco


class DAO():
    @staticmethod
    def getAllNodes():
        conn = DBConnect.get_connection()
        results = []
        cursor = conn.cursor(dictionary=True)
        query = """
                select a.*, count(t.TrackId) as listaBrani
                from album a, track t
                where a.AlbumId = t.AlbumId 
                group by a.AlbumId, a.Title, a.ArtistId 
                having count(distinct t.TrackId) >= 1  
                """
        cursor.execute(query)
        for row in cursor:
            results.append(Album(**row))
        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllEdges(idMap):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """
                select t1.AlbumId as a1, t2.AlbumId as a2
                from (select a.*, t.GenreId
                from album a, track t
                where a.AlbumId = t.AlbumId 
                group by a.AlbumId, a.Title, a.ArtistId 
                having count(distinct t.TrackId) >= 1) as t1, (select a.*, t.GenreId
                from album a, track t
                where a.AlbumId = t.AlbumId 
                group by a.AlbumId, a.Title, a.ArtistId 
                having count(distinct t.TrackId) >= 1) as t2
                where t1.AlbumId < t2.Albumid
                AND EXISTS (
                    SELECT 1
                    FROM track AS tr1, track AS tr2
                    WHERE tr1.AlbumId = t1.AlbumId
                      AND tr2.AlbumId = t2.AlbumId
                      AND tr1.GenreId = tr2.GenreId
                )
                """
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(Arco(idMap[row["a1"]], idMap[row["a2"]]))
        cursor.close()
        cnx.close()
        return result
