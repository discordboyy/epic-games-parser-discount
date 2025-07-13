# epic-games-parser-discount
This is a parser that scrapes current discounts from the Epic Games Store and sorts the results by savings.

epic-games-parser-discount is a Python-based tool that automatically scrapes discounted games from the Epic Games Store using Playwright. It captures game titles, original and discounted prices, calculates savings, and exports the data to Excel and plain text files — sorted by the highest discount.

🚀 Features
Extracts real-time game discount data directly from Epic Games Store.
- Parses and cleans price data (supports multiple currencies).
- Calculates and ranks games by savings.
- Exports results to .xlsx and .txt formats.
- Easy to use and customizable.


🔧 Technologies Used
- Python 3.x
- Playwright – for browser automation
- Pandas – for data handling and Excel export

📂 Output Example
Each result includes:
- ✅ Game Title
- 💲 Original Price
- 🔻 Discounted Price
- 💰 Savings
- 🔗 Direct link to the game page

📎 Use Cases
- Track Epic Games discounts.
- Build a personal game wishlist sorted by savings.
- Generate reports for deals/newsletter content.
