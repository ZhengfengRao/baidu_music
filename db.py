#! /usr/bin/python

# To change this template, choose Tools | Templates
# and open the template in the editor.

import sqlite3

class db:
    def __init__(self):
        self.init_sql = """
            CREATE TABLE if not exists `album` (
            `id` int(11) ,
            `title` varchar(255) DEFAULT NULL,
            `artist` varchar(255) DEFAULT NULL,
            `releasedate` datetime DEFAULT NULL,
            `genres` varchar(255) DEFAULT NULL,
            `releasecompany` varchar(255) DEFAULT NULL,
            `description` text)
            """
        self.exe_count = 0
        self.conn = sqlite3.connect('music.db')
        self.conn.execute(self.init_sql)

    def close(self):
        self.conn.close()

    def add_album(self,id,title,artist,releasedate,genres,company,description):
        try:
            id = id.replace("'", "\\'")
            title = title.replace("'", "\\'")
            artist = artist.replace("'", "\\'")
            releasedate = releasedate.replace("'", "\\'")
            genres = genres.replace("'", "\\'")
            company = company.replace("'", "\\'")
            description = description.replace("'", "\\'")

            add_album_sql = " insert into album(  `id`, `title`, `artist`, `releasedate`, `genres`, `releasecompany`, `description`) values('"
            add_album_sql = add_album_sql + id
            add_album_sql = add_album_sql + "','"
            add_album_sql = add_album_sql + title
            add_album_sql = add_album_sql + "','"
            add_album_sql = add_album_sql + artist
            add_album_sql = add_album_sql + "','"
            add_album_sql = add_album_sql + releasedate
            add_album_sql = add_album_sql + "','"
            add_album_sql = add_album_sql + genres
            add_album_sql = add_album_sql + "','"
            add_album_sql = add_album_sql + company
            add_album_sql = add_album_sql + "','"
            add_album_sql = add_album_sql + description
            add_album_sql = add_album_sql + "')";
            #print add_album_sql
            self.conn.execute(add_album_sql)
            self.conn.commit()
        except Exception, e:
            print "[Error]add_album():",e

