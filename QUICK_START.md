# Roulette Martingale Strategy Tester - Quick Start Guide

## ✅ Application is Running!

Your application is now live and ready to use.

### Access the Application
- **Local**: http://localhost:5000
- **Codespaces**: https://effective-waddle-4qv6v59pqq42jrwv-5000.app.github.dev/

## How to Use

### Method 1: Upload Screenshots

1. **Enter Balance**: Type your initial betting balance (e.g., $1000)
2. **Select Strategy**: Choose "Red/Black Martingale (Strategy-1)"
3. **Upload Screenshot**: 
   - Drag and drop an image of roulette results
   - Or click to browse and select a file
   - Supported formats: PNG, JPG, JPEG, GIF, BMP
4. **Click "Test Strategy"**: Wait for processing
5. **View Results**: See detailed round-by-round breakdown

### Method 2: Use Demo Numbers

1. **Enter Balance**: Type your initial betting balance
2. **In "Demo Numbers" field**: Enter numbers separated by spaces or commas
   - Example: `5 12 18 23 11 30 8 25`
   - Valid numbers: 0-36 (European roulette)
3. **Click "Test Strategy"**: Results show instantly

## Understanding the Results

### Summary Statistics
- **Final Balance**: Your balance after all spins
- **Total Profit/Loss**: Net gain or loss
- **ROI**: Return on Investment percentage
- **Win Rate**: Percentage of winning spins
- **Total Rounds**: Number of spins processed
- **Game Status**: COMPLETED (won) or BUSTED (ran out of money)

### Detailed Rounds Table
Each row shows:
- **Round**: Spin number
- **Number**: Roulette number that appeared
- **Color**: Red, Black, or Green (0)
- **Bet On**: Your betting choice for that round
- **Bet Amount**: Money wagered
- **Result**: WIN or LOSS
- **Win/Loss**: Money gained or lost
- **Balance Changes**: Before and after balance
- **Next Bet**: Amount for next round
- **Next Color**: Strategy for next round
- **Status**: Current game status

## The Martingale Strategy Explained

### How It Works

**Betting Sequence:**
1. Start betting on **RED** with $10
2. **If you WIN**: Keep betting on RED, same $10 bet
3. **If you LOSE**: Switch to BLACK, double the bet to $20
4. **Keep doubling** after each loss until you win
5. **When you win**: Reset to RED with $10 bet

### Example

| Round | Number | Color | Bet On | Bet $ | Result | Balance |
|-------|--------|-------|--------|-------|--------|---------|
| 1     | 5      | Red   | RED    | 10    | WIN    | +1010   |
| 2     | 3      | Red   | RED    | 10    | WIN    | +1020   |
| 3     | 2      | Black | RED    | 10    | LOSS   | -1010   |
| 4     | 14     | Red   | BLACK  | 20    | LOSS   | -990    |
| 5     | 11     | Black | BLACK  | 40    | WIN    | +1030   |

### Why It's Used

The theory: A loss is always followed by a win eventually, so doubling bets recovers losses and makes a profit.

## Features

### 🔍 Search
Use the search box to find specific rounds or numbers

### 📊 Export to CSV
Download your detailed results as a CSV file for Excel analysis

### 📱 Responsive Design
Works on desktop, tablet, and mobile devices

### ⚡ Real-time Processing
See results instantly for demo numbers or after OCR analysis

## Example Screenshots

### Good Screenshot for OCR:
- Clear, large numbers
- Good contrast (dark numbers on light background)
- Numbers arranged in a line or grid
- Minimal noise or clutter

### What Works Best:
- Screenshot from actual roulette display
- Photo of a printed result sheet
- Clear digital display of numbers

### What to Avoid:
- Blurry or low-resolution images
- Very small numbers
- Poor lighting
- Numbers at angles or rotated

## Demo Numbers to Test

```
# Balanced sequence (likely profitable)
18 5 20 12 29 8 31 14 25 10

# Losing streak (bet increases significantly)
3 4 6 8 10 11 13 15 17 20

# All red (very profitable)
1 3 5 7 9 12 14 16 18 19

# Mixed results
25 14 8 23 11 30 5 18 12 29
```

## Troubleshooting

### "Could not extract numbers from screenshot"
- Image quality is too low
- Numbers are unclear or too small
- Try taking a clearer screenshot
- Ensure good lighting and contrast

### "No valid numbers found"
- Numbers entered are outside 0-36 range
- Check for typos in manually entered numbers
- Use space or comma as separator

### Application not responding
- Wait a few seconds for processing
- OCR can take time on large images
- Try with a smaller image or demo numbers

### Balance shows unexpected values
- Check your starting balance
- Verify the numbers were correctly extracted
- Try the same numbers with demo mode to verify

## Important Notes

⚠️ **Educational Tool Only**: This is for testing and learning about betting strategies

⚠️ **Not Guaranteed Profitable**: The Martingale strategy doesn't guarantee profits in real gambling

⚠️ **Risk of Ruin**: Bets double after each loss, leading to rapid balance depletion

⚠️ **Table Limits**: Real casinos have betting limits, which breaks the Martingale strategy

## Tips for Best Results

1. **Test multiple sequences** to see patterns
2. **Start with demo numbers** to understand the strategy
3. **Export results** for detailed analysis
4. **Keep records** to track strategy performance
5. **Understand variance** - short-term results vary

## File Organization

The application creates an `uploads/` directory to temporarily store images during processing. Files are automatically deleted after analysis.

## API Details

### Upload Image
```
POST /api/test-strategy
- balance: number
- strategy: "red_black"
- screenshot: file
```

### Test with Numbers
```
POST /api/test-demo
- balance: number
- strategy: "red_black"
- numbers: [array of numbers]
```

## Next Steps

1. ✅ Application running
2. 📸 Test with demo numbers first
3. 📁 Try uploading a screenshot
4. 📊 Export results
5. 📈 Analyze different strategies

---

**Happy Testing!** 🎰

For more information, check the README.md file in the project root.
