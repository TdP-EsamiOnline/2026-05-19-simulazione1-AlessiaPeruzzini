from model.arco import Arco
from database.DB_connect import DBConnect
from model.artist import Artista
from model.genere import Genere


class DAO():

    @staticmethod
    def getAllGenere():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select *
            from genre"""

        cursor.execute(query)

        for row in cursor:
            results.append(Genere(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllNodes(g):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct a.ArtistId, a.Name
                from artist a, track t, genre g, album a2
                where a.ArtistId = a2.ArtistId and a2.AlbumId = t.AlbumId and t.GenreId = g.GenreId 
                and g.GenreId = %s
                and t.TrackId >=1
                """

        cursor.execute(query,(g.GenreId, ))

        for row in cursor:
            results.append(Artista(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllEdges(g, _idMapP):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct p1.artistid as a1,p2.artistid as a2,p1.n as tip,p2.n as t2p,p1.n + p2.n as peso
                    from
                        (   #CAPIRE SE LO STESSO CLIENTE HA COPRATO DUE ARTISTI
                            select a.ArtistId, i2.CustomerId
                            from artist a, album al, track t, invoiceline i, invoice i2
                            where a.ArtistId = al.ArtistId
                            and al.AlbumId = t.AlbumId
                            and t.TrackId = i.TrackId
                            and i.InvoiceId = i2.InvoiceId
                            and t.GenreId = %s
                            ) as c1,
                                (
                            select a.ArtistId, i2.CustomerId
                            from artist a, album al, track t, invoiceline i, invoice i2
                            where a.ArtistId = al.ArtistId
                            and al.AlbumId = t.AlbumId
                            and t.TrackId = i.TrackId
                            and i.InvoiceId = i2.InvoiceId
                            and t.GenreId = %s
                            ) as c2,
                        (  #CALCOLARE LA POLARITà TOTALE DEI DUE ARTISTI
                        select a.ArtistId, count(*) as n
                        from artist a, album al, track t, invoiceline i, invoice i2
                        where a.ArtistId = al.ArtistId
                        and al.AlbumId = t.AlbumId
                        and t.TrackId = i.TrackId
                        and i.InvoiceId = i2.InvoiceId
                        and t.GenreId = %s
                        group by a.ArtistId
                                ) as p1,
                            (
                        select a.ArtistId, count(*) as n
                        from artist a, album al, track t, invoiceline i, invoice i2
                        where a.ArtistId = al.ArtistId
                            and al.AlbumId = t.AlbumId
                        and t.TrackId = i.TrackId
                        and i.InvoiceId = i2.InvoiceId
                        and t.GenreId = %s
                        group by a.ArtistId
                            ) as p2
                        where c1.CustomerId = c2.CustomerId
                        and c1.ArtistId <> c2.ArtistId
                        and p1.ArtistId = c1.ArtistId
                        and p2.ArtistId = c2.ArtistId
                    and p1.n >= p2.n
                        order by peso desc
                        """

        cursor.execute(query, (g.GenreId, g.GenreId,g.GenreId,g.GenreId))

        for row in cursor:
            results.append(Arco(_idMapP[row["a1"]], _idMapP[row["a2"]], row["peso"]))
        cursor.close()
        conn.close()
        return results
