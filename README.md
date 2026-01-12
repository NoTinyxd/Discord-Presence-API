# Discord-Presence-API

A lightweight Discord bot capable of exposing real-time user presence through a REST API with a clean web interface.

## Features

- Real-time presence tracking of Discord users
- Spotify listening activity with live progress bar
- Game and application activity monitoring
- Custom status display
- Decorations for avatars and profile banners
- Platform detection: desktop, web, mobile
- Discord Profile Badges
- REST API endpoint for easy integration
- Clean web interface using the design language of Discord

## Installation

### 1. Install dependencies:
```bash
pip install discord.py flask flask-cors
```

### 2. Create a config.json file:
```json
{
  "token": "YOUR_BOT_TOKEN_HERE",
  "server_id": "YOUR_SERVER_ID_HERE"
}
```

### 3. Enable proper intents in Discord Developer Portal:
- Presence Intent
- Server Members Intent
- Message Content Intent (in prefix commands)

## Usage
```bash
python main.py
```

The bot will start on two services:
- Discord Bot: connects to your server
- API Server: Runs on http://localhost:5000

## Bot Commands

- `/uptime` or `!uptime` - Display bot uptime with detailed breakdown
- `/link` or `!link` - Obtain your personal API link

## API Endpoint

Access user presence data:
```
GET http://localhost:5000/v1/users/{USER_ID}
```

Returns JSON including user profile, activities and status information.

## Web Interface

Open `examples/example.html` in your browser to see the live presence display.

The interface refreshes every second and displays:
- User avatar with decorations
- Custom status
- Profile Badges
- Main active platform indicators
- Spotify playback if listening
- Game/app activity

## File Structure
```
Discord-Presence-API/
├── bot.py           - Discord bot implementation
├── api.py           - Flask API server
├── main.py          - Application entry point
├── config.json      - Bot configuration
├── examples/
│   ├── example.html - Web interface
│   ├── example.css  - Interface styling
│   └── example.js   - Frontend logic
└── README.md
```

## Requirements

- Python 3.8 or greater
- discord.py
- Flask
- flask-cors

## Disclaimer

This project is for educational purposes. Make sure you follow Discord's Terms of Service and API usage guidelines when using this bot.

## Credits

The credit goes to [https://github.com/Phineas/lanyard](https://github.com/Phineas/lanyard) because it has the core presence service that inspired this project. I just wanted to implement this concept in Python. While the API responses are similar, the Lanyard repository is more mature and feature-rich than this project.

If this repository reaches 100 stars, I may upload a portfolio showcasing projects built using the Lanyard API, or projects based on this repository running on localhost.

## License

MIT
