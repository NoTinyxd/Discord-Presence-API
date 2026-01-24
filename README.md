# Discord-Presence-API

A lightweight Discord bot and REST API that exposes real-time Discord user presence data, including activities, Spotify listening history, profile decorations, and platform status — with a clean Discord-inspired web interface.

## Features

* Real-time presence tracking of Discord users
* Full activity monitoring (games, applications, custom status)
* Spotify listening activity
   * Live playback timestamps
   * Recently played track history
* Custom status support
* Avatar decorations
* Profile banners & accent colors
* Public user flags (`public_flags`)
* Server boost timestamp (`premium_since`)
* Platform detection:
   * Desktop
   * Web
   * Mobile
* Last seen tracking when user goes offline
* REST API endpoint for easy integration
* Per-user rate limiting
* Clean web interface using Discord's design language
* One-click personal API link via Discord command

## ❌ Not Supported

The following features are NOT detected or exposed by this project:

* Nitro / Premium profile badges
* Nitro subscription tier information
* Special event or limited-time badges
* Hidden or legacy Discord badges

> **Note:** `premium_since` should not be relied upon. Server boosting time, Nitro status, and Nitro badges are **not officially supported or guaranteed** by this API.

## Installation

### 1. Install dependencies
```bash
pip install discord.py flask flask-cors
```

### 2. Create a `config.json` file
```json
{
  "token": "YOUR_BOT_TOKEN_HERE",
  "server_id": "YOUR_SERVER_ID_HERE"
}
```

### 3. Enable required intents in the Discord Developer Portal

Enable the following Privileged Gateway Intents:

* Presence Intent
* Server Members Intent
* Message Content Intent (for prefix commands)

## Usage

Start both the Discord bot and the API server:
```bash
python main.py
```

The application runs two services simultaneously:

* **Discord Bot** — tracks user presence and activity
* **API Server** — available at:
```
http://localhost:5000
```

## Bot Commands

* `/link` or `!link` Generates your personal API endpoint with a clickable button.
* `/uptime` or `!uptime` Displays bot uptime with a human-readable breakdown.
* `/help` or `!help` Shows available bot commands.

## API Endpoint

Fetch live Discord presence data for a user:
```
GET /v1/users/{USER_ID}
```

**Example:**
```
http://localhost:5000/v1/users/123456789012345678
```

### API Response Includes

* Discord user profile data
* Avatar & avatar decorations
* Banner & accent color
* Public user flags
* Online status
* Active platforms (desktop, web, mobile)
* Current activities
* Spotify playback data (if listening)
* Recently played Spotify tracks
* Last seen time when offline

Responses are returned as structured JSON.

## Web Interface

Open:
```
examples/example.html
```

The web interface refreshes every second and displays:

* User avatar with decorations
* Custom status
* Public flags
* Active platform indicators
* Spotify playback with progress
* Game / application activity
* Recently played Spotify tracks

## File Structure
```
Discord-Presence-API/
├── bot.py            - Discord bot & presence tracking
├── api.py            - Flask REST API server (all API-related logic)
├── main.py           - Application entry point
├── config.json       - Bot configuration
├── examples/
│   ├── example.html  - Web interface
│   └── example.css   - Interface styling
└── README.md
```

## Requirements

* Python 3.8 or newer
* discord.py
* Flask
* flask-cors

## Disclaimer

This project is for educational purposes only. Ensure you comply with Discord's Terms of Service and API usage guidelines when using or distributing this project.

## Credits

Inspired by **Lanyard** 👉 https://github.com/Phineas/lanyard

This repository provides a self-hosted Python implementation inspired by Lanyard's presence system. Lanyard remains more mature and feature-rich.

**If this repository reaches 100 stars, I may publish:**

* A portfolio of projects built using the Lanyard API
* Example projects using this repository locally

## License

MIT
