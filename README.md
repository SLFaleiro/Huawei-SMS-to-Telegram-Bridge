# Huawei SMS-to-Telegram Bridge

![Python Version](https://img.shields.io/badge/Python-3.7+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Tested Device](https://img.shields.io/badge/Tested%20Device-Huawei%20E3372-brightgreen.svg)

A Python service that forwards SMS messages from Huawei modems to Telegram, with automatic message deletion after forwarding. Specifically tested with the Huawei E3372 USB modem.

## Features

- Automatically authenticates with Huawei modem API
- Retrieves SMS messages using XML API
- Forwards messages to Telegram
- Deletes processed messages from modem
- Comprehensive error logging
- Designed for Huawei modem XML-based API

## Compatible Hardware
Tested with:
- **Product Name**: Huawei
- **Device Name**: E3372
- **Hardware Version**: CL2E3372HM
- **Software Version**: 22.328.62.00.1080
- **Web UI Version**: 17.100.19.04.1080

Should work with other Huawei devices that support:
1. XML-based API at `http://192.168.8.1`
2. Session token authentication
3. Similar SMS endpoints

## Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/huawei-sms-to-telegram.git
   cd huawei-sms-to-telegram
   ```

2. **Configure the script:**
   Edit `sms_bridge.py` with your details:
   ```python
   # Modem configuration (Huawei E3372 default)
   SMS_SERVER_URL = 'http://192.168.8.1'  # Huawei modem default IP
   
   # Telegram configuration
   TELEGRAM_BOT_TOKEN = 'YOUR_BOT_TOKEN'  # From @BotFather
   TELEGRAM_CHAT_ID = 'YOUR_CHAT_ID'     # Group/channel ID
   ```

3. **Create Telegram bot:**
   - Message @BotFather on Telegram
   - Use `/newbot` command
   - Copy the API token

4. **Get Chat ID:**
   - Add bot to your group/channel
   - Visit: `https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates`
   - Look for `chat.id` in JSON response

## Running the Service

### Manual Run:
```bash
python3 sms_bridge.py
```

### As Background Service (Linux):
1. Create systemd service:
   ```bash
   sudo nano /etc/systemd/system/huawei-sms-bridge.service
   ```
2. Add configuration:
   ```ini
   [Unit]
   Description=Huawei SMS to Telegram Bridge
   After=network.target

   [Service]
   User=root
   WorkingDirectory=/path/to/huawei-sms-to-telegram
   ExecStart=/usr/bin/python3 /path/to/huawei-sms-to-telegram/sms_bridge.py
   Restart=always
   RestartSec=10

   [Install]
   WantedBy=multi-user.target
   ```
3. Enable and start:
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable huawei-sms-bridge
   sudo systemctl start huawei-sms-bridge
   ```

## Viewing Logs
```bash
tail -f sms_bridge.log
```

## Huawei E3372 Notes
1. Modem must be in "HiLink" mode (not serial modem mode)
2. Web interface must be accessible at `http://192.168.8.1`
3. The script handles session token management automatically
4. SMS are retrieved from the inbox (BoxType=1)
5. Messages are processed in reverse chronological order (newest first)

## Security Notes
- Ensure your modem's web interface is not exposed to the internet
- Keep Telegram bot token private
- Session tokens are refreshed with each execution
- Consider using HTTPS for Telegram API (already implemented)

## Troubleshooting
| Error | Solution |
|-------|----------|
| 403 Forbidden | Verify session token is valid |
| Connection errors | Check modem IP and connectivity |
| Empty response | Confirm modem has SMS messages |
| XML parsing errors | Check API response format |
| Telegram failures | Verify bot token/chat ID permissions |

## API Endpoints Used
- `GET /api/webserver/SesTokInfo` - Get session token
- `POST /api/sms/sms-list` - Retrieve SMS list
- `POST /api/sms/delete-sms` - Delete SMS by index

## License
MIT License - See [LICENSE](LICENSE) file

---

**Tested Device Information:**  
**Product Name:** Huawei  
**Device Name:** E3372  
**Hardware Version:** CL2E3372HM  
**Software Version:** 22.328.62.00.1080  
**Web UI Version:** 17.100.19.04.1080  

**Note:** Always test with non-critical messages first. Not responsible for lost messages.
