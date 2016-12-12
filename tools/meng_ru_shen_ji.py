#coding:utf-8
import sys
import re
import requests

from bs4 import BeautifulSoup

from tinydb import TinyDB, Query

sys.path.append("..")
from cchess import *

url_base = 'http://www.dpxq.com/hldcg/share/chess_%E8%B1%A1%E6%A3%8B%E8%B0%B1%E5%A4%A7%E5%85%A8/%E8%B1%A1%E6%A3%8B%E8%B0%B1%E5%A4%A7%E5%85%A8-%E5%8F%A4%E8%B0%B1%E6%AE%8B%E5%B1%80/%E6%A2%A6%E5%85%A5%E7%A5%9E%E6%9C%BA/%E6%A2%A6%E5%85%A5%E7%A5%9E%E6%9C%BA/'

games = []

def open_url(url) :
        req = requests.get(url)
        if req.status_code != 200 :
                return None
        return req.content

def parse_games(html) :        
        games = []
        soup = BeautifulSoup(html, 'lxml')
        for td in soup.find_all('td') :
                if td.a == None or len(td.a.text) == 0: 
                        continue
                title = unicode(td.a.text)
                if title.encode('utf-8')[0] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                        #print title, td.a['href'] 
                        games.append([title,  td.a['href']] )
        return games
        
                
html =  open_url(url_base+"1.html")
if html == None :
        sys.exit(-1)
games1 =  parse_games(html.decode("GB2312"))       

html =  open_url(url_base+"2.html")
if html == None :
        sys.exit(-1)
games2 =  parse_games(html.decode("GB2312"))       

games = games1 +games2

games.sort(key=lambda x: x[0])

bad_files = []
db = TinyDB(u'梦入神机.jdb')
for it in games[:] :
        game_info = {}
        html_page = open_url("http://www.dpxq.com" + it[1])
        if html_page == None :      
                continue
        
        game = read_from_dhtml(html_page)
        if not game:
               bad_files.append(it[0])
               continue  
        
        board_txt = game.dump_init_board()
        
        print it[0]
        
        if game.init_board.move_side != ChessSide.RED:
                print "Erorr",game.init_board.move_side 
                break
        
        
        game_info['name']  = it[0][3:]
        game_info['fen']   = game.init_board.to_fen()
        game_info['moves'] = ','.join(game.dump_std_moves()[0])
        db.insert(game_info)
        print
        for line in board_txt:
                print line
        print   
        
        moves = game.dump_std_moves()[0]
        print moves
        moves = game.dump_chinese_moves()[0]
        for it in moves:
                print it,
        print         

db.close()

print "BAD FILES:",
for it in  bad_files:
                print it,
print 'End.'                