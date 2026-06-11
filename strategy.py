"""
Martingale Strategy Implementation for Roulette
Strategy-1: Red/Black Betting with Progressive Doubling
"""

# Roulette wheel: Red and Black numbers
RED_NUMBERS = {1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36}
BLACK_NUMBERS = {2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35}

def is_red(number):
    """Check if number is red"""
    return number in RED_NUMBERS

def is_black(number):
    """Check if number is black"""
    return number in BLACK_NUMBERS

def test_martingale_strategy(initial_balance, numbers):
    """
    Test the Martingale strategy on roulette numbers
    
    Strategy:
    1. Start by betting on Red
    2. If Red wins, continue betting on Red
    3. If Red loses, switch to Black and double the bet
    4. Continue until all numbers are processed
    
    Args:
        initial_balance: Starting balance
        numbers: List of roulette numbers (0-36) in order they appeared
    
    Returns:
        Dictionary with detailed results and round information
    """
    
    if not numbers:
        return {
            'error': 'No numbers to process',
            'success': False
        }
    
    balance = initial_balance
    current_bet = 10  # Starting bet
    current_color = 'red'  # Start betting on red
    rounds = []
    
    for round_num, number in enumerate(numbers, 1):
        # Determine if bet wins
        if current_color == 'red':
            won = is_red(number)
        else:  # black
            won = is_black(number)
        
        # Calculate round details
        if won:
            winnings = current_bet * 2  # In roulette, red/black pays 1:1
            new_balance = balance + current_bet
            result = 'WIN'
            next_color = current_color  # Keep same color on win
            next_bet = 10  # Reset to base bet
        else:
            new_balance = balance - current_bet
            result = 'LOSS'
            # Switch color on loss
            next_color = 'black' if current_color == 'red' else 'red'
            # Double bet for next round on loss
            next_bet = current_bet * 2
        
        # Check if balance is sufficient for next bet
        can_continue = (new_balance > 0)
        if not can_continue and round_num < len(numbers):
            next_bet_status = 'INSUFFICIENT FUNDS'
        else:
            next_bet_status = 'OK'
        
        round_data = {
            'round': round_num,
            'number': number,
            'number_color': 'Red' if is_red(number) else 'Black' if is_black(number) else 'Green (0)',
            'bet_amount': current_bet,
            'bet_on': current_color.upper(),
            'result': result,
            'winnings': current_bet if won else -current_bet,
            'balance_before': balance,
            'balance_after': new_balance,
            'next_bet': next_bet,
            'next_color': next_color.upper(),
            'can_continue': can_continue,
            'status': next_bet_status
        }
        
        rounds.append(round_data)
        
        # Update state for next round
        balance = new_balance
        current_bet = next_bet
        current_color = next_color
        
        # Stop if balance is depleted
        if not can_continue and round_num < len(numbers):
            break
    
    # Calculate statistics
    wins = sum(1 for r in rounds if r['result'] == 'WIN')
    losses = sum(1 for r in rounds if r['result'] == 'LOSS')
    total_profit = balance - initial_balance
    roi = (total_profit / initial_balance * 100) if initial_balance > 0 else 0
    
    return {
        'success': True,
        'initial_balance': initial_balance,
        'final_balance': balance,
        'total_profit': total_profit,
        'roi_percentage': round(roi, 2),
        'total_rounds': len(rounds),
        'wins': wins,
        'losses': losses,
        'win_rate': round(wins / len(rounds) * 100, 2) if rounds else 0,
        'rounds': rounds,
        'game_status': 'COMPLETED' if balance > 0 else 'BUSTED'
    }
