def search_solution(issue):
    text = issue.lower()

    kb = {
        "password": "To reset your password: Press Ctrl + Alt + Delete and choose Change Password.",
        "wifi": "Restart the Wi-Fi adapter, reconnect to the network, then restart your PC.",
        "internet": "Check your network cable or Wi-Fi connection, then restart the router if needed.",
        "printer": "Check printer power, cables, and set it as the default printer.",
        "email": "Check Outlook connection and restart the mail application.",
        "outlook": "Restart Outlook and verify that your internet connection is working.",
        "vpn": "Verify internet connection, then reconnect to the VPN client.",
        "login": "Ensure the correct username/password is used and Caps Lock is off.",
        "pc": "Restart the computer and verify that all cables and power connections are properly connected.",
        "computer": "Restart the computer and verify that all cables and power connections are properly connected.",
        "slow": "Close unnecessary applications, restart the computer, and check available disk space.",
        "frozen": "Press Ctrl + Shift + Esc to open Task Manager and close the unresponsive application.",
        "freeze": "Press Ctrl + Shift + Esc to open Task Manager and close the unresponsive application.",
        "keyboard": "Check keyboard connection or replace batteries if wireless.",
        "mouse": "Reconnect the mouse or replace batteries if wireless.",
        "screen": "Check monitor power and cable connection, then restart the PC.",
        "monitor": "Check monitor power and cable connection, then restart the PC.",
        "blue screen": "Restart the computer. If the issue persists, note the error message and escalate.",
        "usb": "Disconnect and reconnect the USB device, then try another USB port.",
        "audio": "Check speaker/headset connection and verify volume settings.",
        "sound": "Check speaker/headset connection and verify volume settings.",
        "microphone": "Check microphone connection and confirm the correct input device is selected.",
        "teams": "Restart Microsoft Teams and verify your internet connection.",
        "zoom": "Restart Zoom and verify your internet connection."
    }

    for keyword, solution in kb.items():
        if keyword in text:
            return solution

    return "No direct solution found. Please escalate."