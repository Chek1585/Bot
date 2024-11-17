📽️ Telegram Movie Recommendation Bot
📋 Project Description
Telegram Movie Recommendation Bot is a powerful tool that helps users find movies based on various parameters, including year, genre, duration, rating, and more. It supports multiple languages: Russian, English, and German.

✨ Key Features:
Search movies by genre, year, duration, rating, and other parameters.
Generate top-10 rankings for movies, actors, genres, and frequently used words.
Store user preferences and interaction history in a MySQL database for future analysis.
Analyze user activity and provide personalized movie recommendations.
Multilingual interface supporting Russian, English, and German.
🛠️ Technologies and Tools
Programming Language: Python
Telegram API Library: Telebot
Database: MySQL
Additional Libraries:
Regular Expressions (re) for text processing.
Google Sheets for auxiliary data storage and processing.
Power BI for visualizing user activity and trends.
📊 Key Achievements
Implemented user-friendly dialogue logic for seamless interaction.
Integrated MySQL for storing and analyzing user preferences and activity.
Visualized user activity and trends using Power BI dashboards.
Provided stable support for three languages (Russian, English, German).
🚀 Installation and Usage
Clone the repository:
bash
Копировать код
git clone https://github.com/your-repo/telegram-movie-bot.git
Install dependencies:
bash
Копировать код
pip install -r requirements.txt
Configure environment variables: Create a .env file and add the following variables:
makefile
Копировать код
TELEGRAM_API_TOKEN=your_token
MYSQL_HOST=your_host
MYSQL_USER=your_user
MYSQL_PASSWORD=your_password
MYSQL_DB=your_database
Run the bot:
bash
Копировать код
python bot.py
🎯 Usage Examples
Movie search:
User: "Recommend me a comedy movie with a rating above 8."
Bot: "I recommend: Back to the Future (1985), rating 8.5."
Popular actor analysis:
The bot generates a top-10 list of actors most frequently mentioned in user queries.
📧 Contact
Author: Yevhenii
Email: aranitoua@gmail.com
GitHub: https://github.com/Chek1585/Bot
