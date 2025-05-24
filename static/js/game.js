class TicTacToeGame {
    constructor() {
        this.gameId = this.generateGameId();
        this.mode = localStorage.getItem('ttt_mode') || 'ai';
        this.difficulty = 'easy';
        this.player1 = '';
        this.player2 = '';
        this.currentPlayer = 'X';
        this.gameOver = false;
        this.board = Array(9).fill('');
        this.winningLine = null;
        this.history = [];

        this.initializeElements();
        this.attachEventListeners();
        this.setInitialVisibility();
        this.updateCurrentPlayerDisplay();
    }

    generateGameId() {
        return 'game_' + Math.random().toString(36).substr(2, 9);
    }

    initializeElements() {
        this.modeButtons = document.querySelectorAll('.mode-btn');
        this.player1Input = document.getElementById('player1');
        this.player2InputGroup = document.getElementById('player2Input');
        this.player2Input = document.getElementById('player2');
        this.difficultyGroup = document.getElementById('difficultyGroup');
        this.difficultySelect = document.getElementById('difficulty');
        this.botNameLabel = document.getElementById('botName');
        this.startButton = document.getElementById('startGame');
        this.cells = document.querySelectorAll('.cell');
        this.currentPlayerDisplay = document.getElementById('currentPlayer');
        this.historyList = document.getElementById('historyList');
        this.resetHistoryButton = document.getElementById('resetHistory');
        this.resultModal = document.getElementById('resultModal');
        this.resultMessage = document.getElementById('resultMessage');
        this.replayButton = document.getElementById('replayGame');
    }

    attachEventListeners() {
        this.modeButtons.forEach(button => {
            button.addEventListener('click', () => {
                this.handleModeSelection(button);
                this.updateCurrentPlayerDisplay();
                const formError = document.getElementById('formError');
                const gameStatus = document.getElementById('gameStatus');
                formError.textContent = '';
                formError.classList.remove('show');
                gameStatus.textContent = '';
                gameStatus.classList.remove('show', 'hide');
            });
        });
        this.difficultySelect.addEventListener('change', () => {
            this.updateBotName();
            this.updateCurrentPlayerDisplay();
            const formError = document.getElementById('formError');
            const gameStatus = document.getElementById('gameStatus');
            formError.textContent = '';
            formError.classList.remove('show');
            gameStatus.textContent = '';
            gameStatus.classList.remove('show', 'hide');
        });
        this.player1Input.addEventListener('input', () => {
            this.updateCurrentPlayerDisplay();
            const formError = document.getElementById('formError');
            const gameStatus = document.getElementById('gameStatus');
            formError.textContent = '';
            formError.classList.remove('show');
            gameStatus.textContent = '';
            gameStatus.classList.remove('show', 'hide');
        });
        this.player2Input.addEventListener('input', () => {
            this.updateCurrentPlayerDisplay();
            const formError = document.getElementById('formError');
            const gameStatus = document.getElementById('gameStatus');
            formError.textContent = '';
            formError.classList.remove('show');
            gameStatus.textContent = '';
            gameStatus.classList.remove('show', 'hide');
        });
        this.startButton.addEventListener('click', () => this.startGame());
        this.cells.forEach(cell => {
            cell.addEventListener('click', () => {
                this.handleCellClick(cell);
                const gameStatus = document.getElementById('gameStatus');
                gameStatus.classList.remove('show');
                gameStatus.classList.add('hide');
            });
        });
        this.resetHistoryButton.addEventListener('click', () => this.resetHistory());
        this.replayButton.addEventListener('click', () => this.replayGame());
    }

    setInitialVisibility() {
        // Set mode from localStorage
        this.modeButtons.forEach(btn => {
            if (btn.dataset.mode === this.mode) {
                btn.classList.add('active');
            } else {
                btn.classList.remove('active');
            }
        });
        if (this.mode === 'ai') {
            this.player2InputGroup.style.display = 'none';
            this.difficultyGroup.style.display = 'flex';
            this.updateBotName();
        } else {
            this.player2InputGroup.style.display = 'flex';
            this.difficultyGroup.style.display = 'none';
        }
    }

    handleModeSelection(button) {
        this.modeButtons.forEach(btn => btn.classList.remove('active'));
        button.classList.add('active');
        this.mode = button.dataset.mode;
        localStorage.setItem('ttt_mode', this.mode);
        if (this.mode === 'ai') {
            this.player2InputGroup.style.display = 'none';
            this.difficultyGroup.style.display = 'flex';
            this.updateBotName();
        } else {
            this.player2InputGroup.style.display = 'flex';
            this.difficultyGroup.style.display = 'none';
        }
        this.currentPlayer = 'X';
        this.updateCurrentPlayerDisplay();
    }

    updateBotName() {
        const botNames = {
            'easy': 'Ellie',
            'medium': 'Sweety',
            'hard': 'Lexi'
        };
        this.difficulty = this.difficultySelect.value;
        this.botNameLabel.textContent = botNames[this.difficulty] || 'AI';
    }

    async startGame() {
        const formError = document.getElementById('formError');
        const gameStatus = document.getElementById('gameStatus');
        formError.textContent = '';
        formError.classList.remove('show');
        gameStatus.textContent = '';
        gameStatus.classList.remove('show', 'hide');
        const player1Name = this.player1Input.value.trim();
        const player2Name = this.player2Input.value.trim();
        if (this.mode === 'two-player') {
            if (!player1Name && !player2Name) {
                formError.textContent = 'Please enter Player 1 and Player 2 names before starting the game.';
                formError.classList.add('show');
                this.player1Input.focus();
                return;
            } else if (!player1Name) {
                formError.textContent = 'Please enter Player 1 name before starting the game.';
                formError.classList.add('show');
                this.player1Input.focus();
                return;
            } else if (!player2Name) {
                formError.textContent = 'Please enter Player 2 name before starting the game.';
                formError.classList.add('show');
                this.player2Input.focus();
                return;
            }
        } else {
            if (!player1Name) {
                formError.textContent = 'Please enter Player 1 name before starting the game.';
                formError.classList.add('show');
                this.player1Input.focus();
                return;
            }
        }
        // Only set player names after validation
        this.player1 = player1Name;
        this.player2 = this.mode === 'two-player' ? player2Name : this.getBotName();
        if (this.mode === 'ai') {
            this.difficulty = this.difficultySelect.value;
        }
        try {
            const response = await fetch('/api/new-game', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    gameId: this.gameId,
                    mode: this.mode,
                    difficulty: this.difficulty,
                    player1: this.player1,
                    player2: this.player2
                })
            });
            if (response.ok) {
                formError.textContent = '';
                formError.classList.remove('show');
                this.currentPlayer = 'X'; // Always start with X
                this.updateCurrentPlayerDisplay();
                this.resetGame();
                gameStatus.textContent = 'Game Started!';
                gameStatus.classList.add('show');
                gameStatus.classList.remove('hide');
                if (this._gameStatusTimeout) clearTimeout(this._gameStatusTimeout);
                this._gameStatusTimeout = setTimeout(() => {
                    gameStatus.classList.remove('show');
                    gameStatus.classList.add('hide');
                }, 2000);
            }
        } catch (error) {
            formError.textContent = 'Error starting game. Please try again.';
            formError.classList.add('show');
            gameStatus.textContent = '';
            gameStatus.classList.remove('show');
            console.error('Error starting game:', error);
        }
    }

    getBotName() {
        const botNames = {
            'easy': 'Ellie',
            'medium': 'Sweety',
            'hard': 'Lexi'
        };
        return botNames[this.difficulty] || 'AI';
    }

    async handleCellClick(cell) {
        if (this.gameOver || cell.classList.contains('x') || cell.classList.contains('o')) {
            return;
        }
        const position = parseInt(cell.dataset.index);
        try {
            const response = await fetch('/api/move', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    gameId: this.gameId,
                    position: position
                })
            });
            if (response.ok) {
                const data = await response.json();
                this.updateBoard(data);
            }
        } catch (error) {
            console.error('Error making move:', error);
        }
    }

    updateBoard(data) {
        this.board = data.board;
        this.currentPlayer = data.currentPlayer;
        this.gameOver = data.gameOver;
        this.winningLine = data.winningLine;
        this.history = data.history;
        this.updateBoardDisplay();
        this.updateCurrentPlayerDisplay();
        this.updateHistoryDisplay();
        if (this.gameOver) {
            this.showResult(data.result || '');
        }
    }

    updateBoardDisplay() {
        this.cells.forEach((cell, index) => {
            cell.className = 'cell';
            if (this.board[index] === 'X') {
                cell.classList.add('x');
            } else if (this.board[index] === 'O') {
                cell.classList.add('o');
            }
        });
        if (this.winningLine) {
            this.winningLine.forEach(index => {
                this.cells[index].classList.add('winning');
            });
        }
    }

    updateCurrentPlayerDisplay() {
        // Show correct turn label based on mode and input
        let label;
        if (this.mode === 'two-player') {
            const name = this.player1Input.value.trim();
            label = name ? `${name}'s turn` : `Player 1's turn`;
        } else {
            label = `Player X's turn`;
        }
        this.currentPlayerDisplay.textContent = label;
    }

    updateHistoryDisplay() {
        this.historyList.innerHTML = '';
        this.history.forEach(item => {
            const historyItem = document.createElement('div');
            historyItem.className = 'history-item';
            historyItem.textContent = item.result;
            this.historyList.appendChild(historyItem);
        });
    }

    showResult(result) {
        this.resultMessage.textContent = result;
        this.resultModal.classList.add('active');
    }

    async resetHistory() {
        try {
            const response = await fetch('/api/reset-history', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    gameId: this.gameId
                })
            });
            if (response.ok) {
                this.history = [];
                this.updateHistoryDisplay();
            }
        } catch (error) {
            console.error('Error resetting history:', error);
        }
    }

    replayGame() {
        this.resultModal.classList.remove('active');
        this.resetGame();
        this.startGame();
    }

    resetGame() {
        this.currentPlayer = 'X';
        this.gameOver = false;
        this.board = Array(9).fill('');
        this.winningLine = null;
        this.updateBoardDisplay();
        this.updateCurrentPlayerDisplay();
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new TicTacToeGame();
}); 