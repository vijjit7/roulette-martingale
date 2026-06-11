# 🎰 Roulette Martingale Strategy Tester

A web application to test the Martingale progressive betting strategy on historical roulette numbers. Upload screenshots of roulette results or enter numbers manually to see how the strategy performs.

## Features

- **Screenshot Analysis**: Upload images of roulette results and automatically extract numbers using OCR
- **Manual Input**: Enter numbers directly for quick testing
- **Martingale Strategy**: Test the red/black betting strategy with progressive doubling
- **Detailed Results**: View round-by-round calculations showing:
  - Each spin number and color
  - Bet amount and result
  - Balance changes
  - Cumulative profit/loss
- **Summary Statistics**: 
  - Final balance and ROI
  - Win/loss counts and win rate
  - Game status (completed or busted)
- **Export**: Download results as CSV for further analysis

## How the Martingale Strategy Works

1. **Start**: Bet on RED with base bet ($10)
2. **Win**: Continue betting on RED
3. **Loss**: Switch to BLACK and double the bet
4. **Continue**: Repeat until all numbers are processed or balance runs out

## Installation

### Prerequisites
- Python 3.8+
- Tesseract OCR engine (for image processing)

### Ubuntu/Debian
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr python3-pip
```

### macOS
```bash
brew install tesseract
```

### Windows
Download and install from: https://github.com/UB-Mannheim/tesseract/wiki

### Setup

1. Clone the repository
```bash
git clone https://github.com/vijjit7/roulette-martingale.git
cd roulette-martingale
```

2. Create a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install Python dependencies
```bash
pip install -r requirements.txt
```

4. Run the application
```bash
python app.py
```

5. Open your browser and navigate to
```
http://localhost:5000
```

## Usage

### Using Screenshots
1. Enter your initial balance
2. Select the strategy (Red/Black Martingale)
3. Upload a screenshot containing roulette numbers
4. Click "Test Strategy"
5. View detailed results and round-by-round breakdown

### Using Demo Numbers
1. Enter your initial balance
2. Enter numbers directly (space or comma-separated, e.g., `5 12 18 23 11`)
3. Click "Test Strategy"
4. Results will display immediately

## File Structure

```
roulette-martingale/
├── app.py                 # Flask application
├── strategy.py            # Martingale strategy implementation
├── image_processor.py     # OCR and image analysis
├── requirements.txt       # Python dependencies
├── templates/
│   └── index.html        # Main HTML template
└── static/
    ├── style.css         # Styling
    └── script.js         # Frontend logic
```

## Screenshots

### Input Section
- Balance input field
- Strategy selector
- Image upload (drag & drop support)
- Alternative manual number entry

### Results Section
- Summary statistics (final balance, ROI, win rate, etc.)
- Detailed table with round-by-round calculations
- Search functionality to filter rounds
- Export to CSV button

## API Endpoints

### POST /api/test-strategy
Test strategy with screenshot upload
- **multipart/form-data**
  - `balance`: Initial balance (number)
  - `strategy`: Strategy type (string: "red_black")
  - `screenshot`: Image file

### POST /api/test-demo
Test strategy with manual numbers
- **application/json**
  - `balance`: Initial balance (number)
  - `strategy`: Strategy type (string: "red_black")
  - `numbers`: Array of numbers (0-36)

## Response Format

```json
{
  "success": true,
  "initial_balance": 1000,
  "final_balance": 950,
  "total_profit": -50,
  "roi_percentage": -5.0,
  "total_rounds": 10,
  "wins": 6,
  "losses": 4,
  "win_rate": 60.0,
  "game_status": "COMPLETED",
  "rounds": [
    {
      "round": 1,
      "number": 5,
      "number_color": "Red",
      "bet_amount": 10,
      "bet_on": "RED",
      "result": "WIN",
      "winnings": 10,
      "balance_before": 1000,
      "balance_after": 1010,
      "next_bet": 10,
      "next_color": "RED",
      "status": "OK"
    },
    ...
  ]
}
```

## Example Usage

### Example 1: Manual Test
```
Balance: $1000
Numbers: 5 12 18 23 11 30 8 25 14 31
```

### Example 2: Image Upload
1. Take a screenshot of roulette results
2. Upload to the application
3. Numbers are automatically extracted and tested

## Limitations

- OCR accuracy depends on image quality; ensure numbers are clearly visible
- Strategy is for educational/testing purposes only
- Not suitable for actual gambling decisions
- Roulette numbers must be 0-36 (valid European roulette)

## Disclaimer

⚠️ **IMPORTANT**: This is an educational tool for testing betting strategies. Gambling involves significant financial risk and can result in substantial losses. This application is NOT intended for making actual gambling decisions. Results are based on historical data and do not predict future outcomes.

## Future Enhancements

- [ ] Additional betting strategies (Fibonacci, D'Alembert, etc.)
- [ ] Statistical analysis and charts
- [ ] Simulation with random numbers
- [ ] Multi-strategy comparison
- [ ] Database for storing test results
- [ ] Mobile app version

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues or questions, please create an issue on GitHub or contact the maintainer.

---

**Author**: Vijjit Sharma  
**Repository**: https://github.com/vijjit7/roulette-martingale