// DOM Elements
const form = document.getElementById('strategyForm');
const balanceInput = document.getElementById('balance');
const strategySelect = document.getElementById('strategy');
const screenshotInput = document.getElementById('screenshot');
const demoNumbersInput = document.getElementById('demoNumbers');
const loadingIndicator = document.getElementById('loadingIndicator');
const errorMessage = document.getElementById('errorMessage');
const resultsSection = document.getElementById('resultsSection');
const fileInputWrapper = document.querySelector('.file-input-wrapper');
const searchRound = document.getElementById('searchRound');
const exportBtn = document.getElementById('exportBtn');

// Modal elements
const confirmationModal = document.getElementById('confirmationModal');
const confirmBtn = document.getElementById('confirmBtn');
const cancelBtn = document.getElementById('cancelBtn');
const editableNumbers = document.getElementById('editableNumbers');
const extractedNumbersList = document.getElementById('extractedNumbersList');

// Store current form state for later use
let currentFormState = null;

// File input click handler
fileInputWrapper.addEventListener('click', (e) => {
    if (e.target.tagName !== 'INPUT') {
        screenshotInput.click();
    }
});

// File input drag and drop
fileInputWrapper.addEventListener('dragover', (e) => {
    e.preventDefault();
    fileInputWrapper.style.borderColor = '#764ba2';
    fileInputWrapper.style.background = '#f0f0ff';
});

fileInputWrapper.addEventListener('dragleave', (e) => {
    e.preventDefault();
    fileInputWrapper.style.borderColor = '#667eea';
    fileInputWrapper.style.background = '#f9f9f9';
});

fileInputWrapper.addEventListener('drop', (e) => {
    e.preventDefault();
    fileInputWrapper.style.borderColor = '#667eea';
    fileInputWrapper.style.background = '#f9f9f9';
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        screenshotInput.files = files;
        fileInputWrapper.classList.add('has-file');
    }
});

// File input change
screenshotInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
        fileInputWrapper.classList.add('has-file');
    } else {
        fileInputWrapper.classList.remove('has-file');
    }
});

// Form submission
form.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    // Reset UI
    hideError();
    hideResults();
    
    const balance = parseFloat(balanceInput.value);
    const strategy = strategySelect.value;
    const demoNumbers = demoNumbersInput.value.trim();
    const hasScreenshot = screenshotInput.files.length > 0;
    
    // Validation
    if (balance <= 0) {
        showError('Balance must be greater than 0');
        return;
    }
    
    if (!hasScreenshot && !demoNumbers) {
        showError('Please upload a screenshot or enter demo numbers');
        return;
    }
    
    showLoading();
    
    try {
        if (demoNumbers) {
            // Use demo numbers directly
            const numbers = parseNumbers(demoNumbers);
            if (numbers.length === 0) {
                showError('No valid numbers found. Use numbers 0-36 separated by space or comma.');
                hideLoading();
                return;
            }
            
            const response = await fetch('/api/test-demo', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    balance,
                    strategy,
                    numbers
                })
            });

            const data = await response.json();
            hideLoading();
            
            if (!response.ok || data.error) {
                showError(data.error || 'An error occurred');
                return;
            }
            
            displayResults(data);
        } else if (hasScreenshot) {
            // Extract numbers from screenshot first
            const formData = new FormData();
            formData.append('screenshot', screenshotInput.files[0]);
            
            const response = await fetch('/api/extract-numbers', {
                method: 'POST',
                body: formData
            });
            
            const data = await response.json();
            hideLoading();
            
            if (!response.ok || data.error) {
                showError(data.error || 'An error occurred');
                return;
            }
            
            // Store form state and show confirmation modal
            currentFormState = {
                balance,
                strategy,
                numbers: data.numbers
            };
            
            showConfirmationModal(data.numbers);
        }
    } catch (error) {
        hideLoading();
        showError(`Network error: ${error.message}`);
    }
});

// Modal handlers
confirmBtn.addEventListener('click', async () => {
    const editedText = editableNumbers.value.trim();
    let finalNumbers;
    
    if (editedText) {
        finalNumbers = parseNumbers(editedText);
        if (finalNumbers.length === 0) {
            alert('Please enter valid numbers (0-36) separated by space or comma');
            return;
        }
    } else {
        finalNumbers = currentFormState.numbers;
    }
    
    hideConfirmationModal();
    
    // Now run the test with confirmed numbers
    showLoading();
    
    try {
        const response = await fetch('/api/test-demo', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                balance: currentFormState.balance,
                strategy: currentFormState.strategy,
                numbers: finalNumbers
            })
        });
        
        const data = await response.json();
        hideLoading();
        
        if (!response.ok || data.error) {
            showError(data.error || 'An error occurred');
            return;
        }
        
        displayResults(data);
    } catch (error) {
        hideLoading();
        showError(`Network error: ${error.message}`);
    }
});

cancelBtn.addEventListener('click', () => {
    hideConfirmationModal();
});

// Close modal when clicking outside
confirmationModal.addEventListener('click', (e) => {
    if (e.target === confirmationModal) {
        hideConfirmationModal();
    }
});

// Helper Functions
function parseNumbers(input) {
    // Split by space or comma
    const parts = input.replace(/,/g, ' ').split(/\s+/);
    const numbers = [];
    
    for (const part of parts) {
        if (part === '') continue;
        const num = parseInt(part);
        if (!isNaN(num) && num >= 0 && num <= 36) {
            numbers.push(num);
        }
    }
    
    return numbers;
}

function showLoading() {
    loadingIndicator.classList.remove('hidden');
}

function hideLoading() {
    loadingIndicator.classList.add('hidden');
}

function showError(message) {
    errorMessage.textContent = message;
    errorMessage.classList.remove('hidden');
    errorMessage.scrollIntoView({ behavior: 'smooth' });
}

function hideError() {
    errorMessage.classList.add('hidden');
}

function hideResults() {
    resultsSection.classList.add('hidden');
}

function displayResults(data) {
    // Update summary stats
    const finalBalance = data.final_balance;
    const totalProfit = data.total_profit;
    const roi = data.roi_percentage;
    const winRate = data.win_rate;
    
    document.getElementById('finalBalance').textContent = formatCurrency(finalBalance);
    document.getElementById('finalBalance').className = `stat-value ${totalProfit >= 0 ? 'positive' : 'negative'}`;
    
    document.getElementById('totalProfit').textContent = formatCurrency(totalProfit);
    document.getElementById('totalProfit').className = `stat-value ${totalProfit >= 0 ? 'positive' : 'negative'}`;
    
    document.getElementById('roi').textContent = `${roi}%`;
    document.getElementById('roi').className = `stat-value ${roi >= 0 ? 'positive' : 'negative'}`;
    
    document.getElementById('winRate').textContent = `${winRate}%`;
    document.getElementById('totalRounds').textContent = data.total_rounds;
    document.getElementById('gameStatus').textContent = data.game_status;
    document.getElementById('gameStatus').className = `stat-value ${data.game_status === 'COMPLETED' ? 'positive' : 'negative'}`;
    
    // Display detailed rounds
    displayRounds(data.rounds);
    
    // Show results section
    resultsSection.classList.remove('hidden');
    resultsSection.scrollIntoView({ behavior: 'smooth' });
}

function displayRounds(rounds) {
    const roundsTable = document.getElementById('roundsTable');
    
    let html = `
        <table>
            <thead>
                <tr>
                    <th>Round</th>
                    <th>Number</th>
                    <th>Color</th>
                    <th>Bet On</th>
                    <th>Bet Amount</th>
                    <th>Result</th>
                    <th>Win/Loss</th>
                    <th>Balance Before</th>
                    <th>Balance After</th>
                    <th>Next Bet</th>
                    <th>Next Color</th>
                    <th>Status</th>
                </tr>
            </thead>
            <tbody>
    `;
    
    for (const round of rounds) {
        const rowClass = round.result === 'WIN' ? 'win' : 'loss';
        const resultBadge = `<span class="badge ${round.result.toLowerCase()}">${round.result}</span>`;
        const colorBadge = `<span class="badge ${round.number_color.toLowerCase()}">${round.number_color}</span>`;
        const betOnBadge = `<span class="badge ${round.bet_on.toLowerCase()}">${round.bet_on}</span>`;
        const nextColorBadge = `<span class="badge ${round.next_color.toLowerCase()}">${round.next_color}</span>`;
        
        const winloss = round.winnings >= 0 ? `+${formatCurrency(round.winnings)}` : formatCurrency(round.winnings);
        const winlossClass = round.winnings >= 0 ? 'positive' : 'negative';
        
        html += `
            <tr class="${rowClass}">
                <td><strong>${round.round}</strong></td>
                <td><strong>${round.number}</strong></td>
                <td>${colorBadge}</td>
                <td>${betOnBadge}</td>
                <td>${formatCurrency(round.bet_amount)}</td>
                <td>${resultBadge}</td>
                <td class="${winlossClass}">${winloss}</td>
                <td>${formatCurrency(round.balance_before)}</td>
                <td><strong>${formatCurrency(round.balance_after)}</strong></td>
                <td>${formatCurrency(round.next_bet)}</td>
                <td>${nextColorBadge}</td>
                <td>${round.status}</td>
            </tr>
        `;
    }
    
    html += `
            </tbody>
        </table>
    `;
    
    roundsTable.innerHTML = html;
    
    // Store rounds data for search and export
    roundsTable.dataset.rounds = JSON.stringify(rounds);
}

function formatCurrency(value) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
    }).format(value);
}

// Search functionality
searchRound.addEventListener('input', (e) => {
    const searchValue = e.target.value.toLowerCase();
    const table = document.querySelector('.rounds-table table');
    
    if (!table) return;
    
    const rows = table.querySelectorAll('tbody tr');
    
    rows.forEach(row => {
        const text = row.textContent.toLowerCase();
        row.style.display = text.includes(searchValue) ? '' : 'none';
    });
});

// Export to CSV functionality
exportBtn.addEventListener('click', () => {
    const roundsTable = document.getElementById('roundsTable');
    const roundsData = JSON.parse(roundsTable.dataset.rounds || '[]');
    
    if (roundsData.length === 0) return;
    
    // Prepare CSV data
    const headers = [
        'Round', 'Number', 'Color', 'Bet On', 'Bet Amount', 'Result',
        'Win/Loss', 'Balance Before', 'Balance After', 'Next Bet', 'Next Color', 'Status'
    ];
    
    let csv = headers.join(',') + '\n';
    
    for (const round of roundsData) {
        const row = [
            round.round,
            round.number,
            round.number_color,
            round.bet_on,
            round.bet_amount,
            round.result,
            round.winnings,
            round.balance_before,
            round.balance_after,
            round.next_bet,
            round.next_color,
            round.status
        ];
        csv += row.map(val => `"${val}"`).join(',') + '\n';
    }
    
    // Download CSV
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `roulette-strategy-${new Date().toISOString().slice(0, 10)}.csv`;
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
    document.body.removeChild(a);
});

// Modal helper functions
function showConfirmationModal(numbers) {
    // Display extracted numbers as badges
    extractedNumbersList.innerHTML = '';
    numbers.forEach(num => {
        const badge = document.createElement('div');
        badge.className = 'number-badge';
        badge.textContent = num;
        extractedNumbersList.appendChild(badge);
    });
    
    // Pre-fill the textarea with the extracted numbers
    editableNumbers.value = numbers.join(' ');
    
    // Show modal
    confirmationModal.classList.remove('hidden');
    confirmationModal.scrollIntoView({ behavior: 'smooth' });
    editableNumbers.focus();
}

function hideConfirmationModal() {
    confirmationModal.classList.add('hidden');
    editableNumbers.value = '';
    extractedNumbersList.innerHTML = '';
}
