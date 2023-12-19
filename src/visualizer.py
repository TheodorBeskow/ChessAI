from flask import Flask, Response, render_template, jsonify, request
import time
import chess, chess.svg
import random
import importlib.util
import requests

app = Flask(__name__)

spec1 = importlib.util.spec_from_file_location("bot1", "src/bot1/search.py")
bot1_module = importlib.util.module_from_spec(spec1)
spec1.loader.exec_module(bot1_module)
bot1 = bot1_module.Bot()

spec2 = importlib.util.spec_from_file_location("bot2", "src/bot2/search.py")
bot2_module = importlib.util.module_from_spec(spec2)
spec2.loader.exec_module(bot2_module)
bot2 = bot2_module.Bot()

board = chess.Board()


@app.route('/', methods =['GET', 'POST'])
def index():
    html = '''<html>
    <head>
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.7.1/jquery.min.js"></script>
        <!-- <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}"> -->
        <style>
            body {
                background-color: #555555;
            }
            .button {
                background-color: #04AA6D;
                /* background-color: #555555; */
                border: none;
                color: white;
                padding: 15px 32px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 16px;
                margin: 4px 2px;
                cursor: pointer;
                border-radius: 8px;
            }
            input[type=text] {
                /* width: 100%; */
                padding: 12px 20px;
                margin: 8px 8px;
                box-sizing: border-box;
                border: 2px solid #04AA6D;
                border-radius: 4px;
            }
        </style>
    </head>
    <body>
'''
    
    html += '<img id="board" width=600 height=600 src="/board"></img>'
    
    html += '''<div><input type="text" id="input_string" placeholder="Play move vs bot" onkeydown="if(event.keyCode==13) {event.preventDefault(); $.post('/play', {mov: document.getElementById('input_string').value}, function() { $('#board').attr('src', '/board?' + new Date().getTime()); $('#input_string').val(''); });}">''' 
    # html += '<div><button class="button" onclick=\'$.post("/move", function() { $("#board").attr("src", "/board?" + new Date().getTime()); });\'>Play bot</button>'
    
    html += '''<button class="button" onclick="self_play()">Self Play</button>        
            
             <script>
                var self_play_interval;
                function self_play() {
                    $.post("/move", function() {
                        var timestamp = new Date().getTime();
                        var board_url = "/board?" + timestamp;
                        $("#board").attr("src", board_url);
                        self_play_interval = setTimeout(self_play, 100);
                        localStorage.setItem('self_play_interval', self_play_interval);
                    });
                }
                
                function stop_self_play() {
                    clearTimeout(self_play_interval);
                    localStorage.removeItem('self_play_interval');
                }
                
                $(document).ready(function() {
                    var self_play_interval = localStorage.getItem('self_play_interval');
                    if (self_play_interval) {
                        self_play_interval = parseInt(self_play_interval);
                        self_play_interval = setTimeout(self_play, 100);
                    }
                });
            </script>
               
            '''
            
    
    
    html += '<button class="button" onclick=\'$.post("/reset", function() { $("#board").attr("src", "/board?" + new Date().getTime()); stop_self_play(); });\'>RESET</button></div>'

    return html

@app.route('/board', methods=['GET'])
def showBoard(): 
    return Response(chess.svg.board(board=board, size=600) , mimetype='image/svg+xml')

@app.route('/move', methods = ["POST"])
def move():
    if not board.is_game_over():
        if board.turn:
            print("innan")
            move = bot1.choose_move(board)
            print(move)
        else:
            move = bot2.choose_move(board)
            time.sleep(1)
        board.push(move)
        
    return ""

@app.route('/reset', methods = ["POST"])
def reset():
    board.reset()
    # board.set_fen("8/8/8/8/5K1k/8/6Q1/8 w - - 0 1")
    return ""

@app.route('/play', methods = ["GET", "POST"])

def play():
    mov = request.form.get('mov')
    # if mov not in list(board.legal_moves):
    #     return ""
    if not board.is_game_over():
        board.push_san(mov)
        board.push(bot1.choose_move(board))
    
    return ""


if __name__ == '__main__':
    app.run(debug = True)