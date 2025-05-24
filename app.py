"""

████████ ██  ██████     ████████  █████   ██████     ████████  ██████  ███████ 
   ██    ██ ██             ██    ██   ██ ██             ██    ██    ██ ██      
   ██    ██ ██             ██    ███████ ██             ██    ██    ██ █████   
   ██    ██ ██             ██    ██   ██ ██             ██    ██    ██ ██      
   ██    ██  ██████        ██    ██   ██  ██████        ██     ██████  ███████ 
                                                                               
                                                                               

TIC TAC TOE - Python Flask Web App
==================================

Project Overview:
-----------------
This project is a modern, full-featured Tic Tac Toe web application built with Python (Flask) for the backend and HTML/CSS/JavaScript for the frontend. It supports both single-player (vs AI) and two-player modes, with three AI difficulty levels and a clean, minimal UI.

Game Rules:
-----------
- The game is played on a 3x3 grid.
- Players take turns placing X or O in empty squares.
- The first player to get three of their marks in a row (vertically, horizontally, or diagonally) wins.
- If all 9 squares are filled and no player has three in a row, the game is a draw.

API Reference:
--------------
1. GET `/`
   - Returns the main HTML page for the game UI.

2. POST `/api/new-game`
   - Starts a new game session.
   - Request JSON: `{ "gameId": str, "mode": "ai"|"two-player", "difficulty": "easy"|"medium"|"hard", "player1": str, "player2": str }`
   - Response: `{ "status": "success" }`

3. POST `/api/move`
   - Makes a move for the current player (and AI if in AI mode).
   - Request JSON: `{ "gameId": str, "position": int }`
   - Response: `{ "status": "success", "board": [str], "currentPlayer": str, "gameOver": bool, "winner": str|None, "winningLine": [int]|None, "result": str, "history": [ {"winner": str, "result": str} ] }`

4. POST `/api/reset-history`
   - Resets the match history for the current game.
   - Request JSON: `{ "gameId": str }`
   - Response: `{ "status": "success" }`

AI Difficulty Levels:
---------------------
- Easy (Ellie): Random moves.
- Medium (Blake): Tries to win or block, otherwise random.
- Hard (Lexi): Uses minimax algorithm (unbeatable).

Example API Request/Response:
-----------------------------
POST /api/move
Request: { "gameId": "game_abc123", "position": 4 }
Response: {
  "status": "success",
  "board": ["X", "O", "X", "", "O", "", "", "", "X"],
  "currentPlayer": "O",
  "gameOver": false,
  "winner": null,
  "winningLine": null,
  "result": null,
  "history": [ {"winner": "X", "result": "You win!"} ]
}

Game Flow:
----------
1. User opens the web app and selects mode/difficulty.
2. User enters player names and clicks Start Game.
3. The frontend sends a POST to `/api/new-game` to initialize the game.
4. Players (or player and AI) take turns making moves via `/api/move`.
5. The backend checks for a winner or draw after each move and responds with the updated state.
6. When the game ends, the result is shown and added to match history.
7. Users can reset the match history or start a new game at any time.

AI Logic Details:
-----------------
- Easy: Picks a random empty cell.
- Medium: Checks if it can win in one move, then if it needs to block, otherwise random.
- Hard: Uses minimax to evaluate all possible outcomes and always plays optimally.

Frontend-Backend Interaction:
-----------------------------
- The frontend uses AJAX (fetch) to communicate with the backend for all game actions.
- The backend responds with JSON, and the frontend updates the UI accordingly.
- All game logic and state are managed in Python; the JS is only for UI and API calls.

Changelog:
----------
- v1.0: Initial release with AI and two-player mode.
- v1.1: Added match history and reset feature.
- v1.2: Improved UI, added detailed documentation.

Frequently Asked Questions (FAQ):
---------------------------------
Q: Can I play against an unbeatable AI?
A: Yes! Select "Hard (Lexi)" for the minimax AI.

Q: Is my match history saved if I refresh?
A: No, history is stored in memory per session.

Q: Can I add more features?
A: Yes! The code is organized for easy extension.

Q: What happens if I try to move in a filled cell?
A: The backend will reject the move and return an error.

Q: Can I use this as a template for other games?
A: Absolutely! The structure is modular and easy to adapt.

Contributing:
-------------
- Fork the repo, make your changes, and submit a pull request.
- Please add tests and update documentation for new features.

Contact:
--------
For questions or suggestions, open an issue or contact the maintainer.

"""
from flask import Flask, render_template, request, jsonify
import random
import json
from pathlib import Path

app = Flask(__name__)

# Game state storage
game_states = {}

class TicTacToe:
    def __init__(self):
        self.board = ['' for _ in range(9)]
        self.current_player = 'X'
        self.winner = None
        self.game_over = False
        self.winning_line = None

    def make_move(self, position):
        if self.board[position] == '' and not self.game_over:
            self.board[position] = self.current_player
            self.check_winner()
            if not self.game_over:
                self.current_player = 'O' if self.current_player == 'X' else 'X'
            return True
        return False

    def check_winner(self):
        winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6]  # Diagonals
        ]

        for combo in winning_combinations:
            if (self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]] != ''):
                self.winner = self.board[combo[0]]
                self.game_over = True
                self.winning_line = combo
                return

        if '' not in self.board:
            self.game_over = True

    def get_ai_move(self, difficulty):
        if difficulty == 'easy':
            return self._get_random_move()
        elif difficulty == 'medium':
            return self._get_medium_move()
        else:  # hard
            return self._get_minimax_move()

    def _get_random_move(self):
        empty_positions = [i for i, spot in enumerate(self.board) if spot == '']
        return random.choice(empty_positions) if empty_positions else None

    @staticmethod
    def check_winner_on_board(board):
        winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ]
        for combo in winning_combinations:
            if board[combo[0]] == board[combo[1]] == board[combo[2]] != '':
                return board[combo[0]]
        if '' not in board:
            return 'draw'
        return None

    def _get_medium_move(self):
        # Try to win or block opponent using pure board logic
        for player in ['O', 'X']:
            for i in range(9):
                if self.board[i] == '':
                    temp_board = self.board[:]
                    temp_board[i] = player
                    winner = self.check_winner_on_board(temp_board)
                    if winner == player:
                        return i
        return self._get_random_move()

    def _get_minimax_move(self):
        best_score = float('-inf')
        best_move = None
        for i in range(9):
            if self.board[i] == '':
                temp_board = self.board[:]
                temp_board[i] = 'O'
                score = self._minimax(temp_board, 0, False)
                if score > best_score:
                    best_score = score
                    best_move = i
        return best_move

    def _minimax(self, board, depth, is_maximizing):
        winner = self.check_winner_on_board(board)
        if winner == 'O':
            return 1
        elif winner == 'X':
            return -1
        elif winner == 'draw':
            return 0
        if is_maximizing:
            best_score = float('-inf')
            for i in range(9):
                if board[i] == '':
                    board[i] = 'O'
                    score = self._minimax(board, depth + 1, False)
                    board[i] = ''
                    best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for i in range(9):
                if board[i] == '':
                    board[i] = 'X'
                    score = self._minimax(board, depth + 1, True)
                    board[i] = ''
                    best_score = min(score, best_score)
            return best_score

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/new-game', methods=['POST'])
def new_game():
    data = request.json
    game_id = data.get('gameId')
    mode = data.get('mode')
    difficulty = data.get('difficulty', 'easy')
    
    game_states[game_id] = {
        'game': TicTacToe(),
        'mode': mode,
        'difficulty': difficulty,
        'player1': data.get('player1', 'Player 1'),
        'player2': data.get('player2', 'Player 2'),
        'history': []
    }
    
    return jsonify({'status': 'success'})

@app.route('/api/move', methods=['POST'])
def make_move():
    data = request.json
    game_id = data.get('gameId')
    position = data.get('position')
    
    if game_id not in game_states:
        return jsonify({'error': 'Game not found'}), 404
    
    game_state = game_states[game_id]
    game = game_state['game']
    
    if game.make_move(position):
        if game.game_over:
            if game_state['mode'] == 'ai':
                bot_names = {'easy': 'Ellie', 'medium': 'Blake', 'hard': 'Lexi'}
                bot_name = bot_names.get(game_state['difficulty'], 'AI')
                if game.winner == 'X':
                    result = "You win!"
                elif game.winner == 'O':
                    result = f"{bot_name} wins!"
                else:
                    result = "It's a draw!"
            else:
                if game.winner:
                    result = f"{game_state['player1'] if game.winner == 'X' else game_state['player2']} wins!"
                else:
                    result = "It's a draw!"
            game_state['history'].append({
                'winner': game.winner,
                'result': result
            })
            # Keep only last 5 matches
            game_state['history'] = game_state['history'][-5:]
            return jsonify({
                'status': 'success',
                'board': game.board,
                'gameOver': True,
                'winner': game.winner,
                'winningLine': game.winning_line,
                'result': result,
                'history': game_state['history']
            })
        
        # If it's AI's turn
        if game_state['mode'] == 'ai' and game.current_player == 'O' and not game.game_over:
            ai_move = game.get_ai_move(game_state['difficulty'])
            if ai_move is not None:
                game.make_move(ai_move)
                if game.game_over:
                    bot_names = {'easy': 'Ellie', 'medium': 'Blake', 'hard': 'Lexi'}
                    bot_name = bot_names.get(game_state['difficulty'], 'AI')
                    if game.winner == 'X':
                        result = "You win!"
                    elif game.winner == 'O':
                        result = f"{bot_name} wins!"
                    else:
                        result = "It's a draw!"
                    game_state['history'].append({
                        'winner': game.winner,
                        'result': result
                    })
                    game_state['history'] = game_state['history'][-5:]
                    return jsonify({
                        'status': 'success',
                        'board': game.board,
                        'currentPlayer': game.current_player,
                        'gameOver': game.game_over,
                        'winner': game.winner,
                        'winningLine': game.winning_line,
                        'result': result,
                        'history': game_state['history']
                    })
        return jsonify({
            'status': 'success',
            'board': game.board,
            'currentPlayer': game.current_player,
            'gameOver': game.game_over,
            'winner': game.winner,
            'winningLine': game.winning_line,
            'history': game_state['history']
        })
    
    return jsonify({'error': 'Invalid move'}), 400

@app.route('/api/reset-history', methods=['POST'])
def reset_history():
    data = request.json
    game_id = data.get('gameId')
    
    if game_id in game_states:
        game_states[game_id]['history'] = []
        return jsonify({'status': 'success'})
    
    return jsonify({'error': 'Game not found'}), 404

if __name__ == '__main__':
    app.run(debug=True) 