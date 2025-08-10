# Samsung TV Remote Control Commands

This document lists all the available commands that can be sent to Samsung TVs using the samsung_remote control system.

## Basic Navigation Commands

### Directional Keys
- `KEY_UP` - Navigate up in menus
- `KEY_DOWN` - Navigate down in menus
- `KEY_LEFT` - Navigate left in menus
- `KEY_RIGHT` - Navigate right in menus
- `KEY_ENTER` - Select/confirm current item
- `KEY_RETURN` - Go back/return to previous menu

### Menu Navigation
- `KEY_MENU` - Open main menu
- `KEY_HOME` - Go to home screen
- `KEY_SOURCE` - Open source selection
- `KEY_GUIDE` - Open program guide
- `KEY_INFO` - Display information
- `KEY_TOOLS` - Open tools menu

## Power and System Commands

### Power Control
- `KEY_POWER` - Toggle power on/off
- `KEY_POWEROFF` - Turn off TV
- `KEY_POWERON` - Turn on TV

### System Commands
- `KEY_EXIT` - Exit current application/menu
- `KEY_CANCEL` - Cancel current operation
- `KEY_BACK` - Go back (same as KEY_RETURN)

## Volume and Audio Commands

### Volume Control
- `KEY_VOLUP` - Increase volume
- `KEY_VOLDOWN` - Decrease volume
- `KEY_MUTE` - Toggle mute on/off

### Audio Settings
- `KEY_AUDIO` - Open audio settings
- `KEY_SUBTITLE` - Toggle subtitles
- `KEY_AD` - Audio description

## Channel Commands

### Channel Navigation
- `KEY_CHUP` - Next channel
- `KEY_CHDOWN` - Previous channel
- `KEY_CH_LIST` - Open channel list
- `KEY_FAVCH` - Favorite channels

### Channel Numbers
- `KEY_0` through `KEY_9` - Number keys for direct channel entry
- `KEY_DASH` - Dash/minus for channel numbers (e.g., 12-1)

## Media Playback Commands

### Playback Control
- `KEY_PLAY` - Play media
- `KEY_PAUSE` - Pause media
- `KEY_STOP` - Stop media
- `KEY_FF` - Fast forward
- `KEY_REWIND` - Rewind
- `KEY_PREV` - Previous track/chapter
- `KEY_NEXT` - Next track/chapter

### Media Functions
- `KEY_REC` - Record
- `KEY_LIVE` - Live TV
- `KEY_EPG` - Electronic Program Guide

## Smart TV and App Commands

### Smart Features
- `KEY_SMART_HUB` - Open Smart Hub
- `KEY_APPS` - Open apps menu
- `KEY_BROWSER` - Open web browser
- `KEY_SEARCH` - Open search function

### App Navigation
- `KEY_APPS_UP` - Navigate up in apps
- `KEY_APPS_DOWN` - Navigate down in apps
- `KEY_APPS_LEFT` - Navigate left in apps
- `KEY_APPS_RIGHT` - Navigate right in apps

## Picture and Display Commands

### Picture Settings
- `KEY_PICTURE_SIZE` - Change picture size/aspect ratio
- `KEY_PICTURE_MODE` - Change picture mode
- `KEY_BRIGHTNESS` - Adjust brightness
- `KEY_CONTRAST` - Adjust contrast

### Display Functions
- `KEY_SCREEN_MODE` - Change screen mode
- `KEY_ASPECT_RATIO` - Change aspect ratio
- `KEY_ZOOM` - Zoom in/out

## Input and Source Commands

### Input Selection
- `KEY_HDMI1` - Select HDMI 1
- `KEY_HDMI2` - Select HDMI 2
- `KEY_HDMI3` - Select HDMI 3
- `KEY_HDMI4` - Select HDMI 4
- `KEY_AV1` - Select AV 1
- `KEY_AV2` - Select AV 2
- `KEY_COMPONENT1` - Select Component 1
- `KEY_COMPONENT2` - Select Component 2

### Source Functions
- `KEY_SOURCE_HDMI1` - Switch to HDMI 1
- `KEY_SOURCE_HDMI2` - Switch to HDMI 2
- `KEY_SOURCE_HDMI3` - Switch to HDMI 3
- `KEY_SOURCE_HDMI4` - Switch to HDMI 4

## Text and Input Commands

### Text Input
- `KEY_RED` - Red button (context sensitive)
- `KEY_GREEN` - Green button (context sensitive)
- `KEY_YELLOW` - Yellow button (context sensitive)
- `KEY_BLUE` - Blue button (context sensitive)

### Special Functions
- `KEY_3D` - Toggle 3D mode
- `KEY_3SPEED` - 3-speed playback
- `KEY_ANYNET` - Anynet+ (HDMI-CEC)
- `KEY_ANYVIEW` - Anyview mode

## Gaming and Special Commands

### Gaming Functions
- `KEY_GAME` - Game mode
- `KEY_INTERNET` - Internet browser
- `KEY_IPLUS` - i+ (interactive plus)

### Special Features
- `KEY_CC` - Closed captions
- `KEY_DTV` - Digital TV
- `KEY_DTV_LINK` - DTV Link
- `KEY_ENTER` - Enter key
- `KEY_ESAVING` - Energy saving
- `KEY_FACTORY` - Factory reset (use with caution)
- `KEY_FAST_FWD` - Fast forward
- `KEY_FM_RADIO` - FM Radio
- `KEY_HELP` - Help
- `KEY_INSREPEAT` - Instant replay
- `KEY_LEFT` - Left arrow
- `KEY_LINK` - Link
- `KEY_MTS` - MTS (Multi-channel Television Sound)
- `KEY_OFF_TIMER` - Off timer
- `KEY_ON_TIMER` - On timer
- `KEY_PANEL_CH_UP` - Panel channel up
- `KEY_PANEL_CH_DOWN` - Panel channel down
- `KEY_PANEL_ENTER` - Panel enter
- `KEY_PANEL_MENU` - Panel menu
- `KEY_PANEL_POWER` - Panel power
- `KEY_PANEL_SOURCE` - Panel source
- `KEY_PANEL_VOL_UP` - Panel volume up
- `KEY_PANEL_VOL_DOWN` - Panel volume down
- `KEY_PANEL_UP` - Panel up
- `KEY_PANEL_DOWN` - Panel down
- `KEY_PANEL_LEFT` - Panel left
- `KEY_PANEL_RIGHT` - Panel right
- `KEY_PANEL_ENTER` - Panel enter
- `KEY_PANEL_RETURN` - Panel return
- `KEY_PANEL_CH_LIST` - Panel channel list
- `KEY_PANEL_FAVCH` - Panel favorite channel
- `KEY_PANEL_MENU` - Panel menu
- `KEY_PANEL_SOURCE` - Panel source
- `KEY_PANEL_GUIDE` - Panel guide
- `KEY_PANEL_INFO` - Panel info
- `KEY_PANEL_TOOLS` - Panel tools
- `KEY_PANEL_UP` - Panel up
- `KEY_PANEL_DOWN` - Panel down
- `KEY_PANEL_LEFT` - Panel left
- `KEY_PANEL_RIGHT` - Panel right
- `KEY_PANEL_ENTER` - Panel enter
- `KEY_PANEL_RETURN` - Panel return
- `KEY_PANEL_CH_LIST` - Panel channel list
- `KEY_PANEL_FAVCH` - Panel favorite channel
- `KEY_PANEL_MENU` - Panel menu
- `KEY_PANEL_SOURCE` - Panel source
- `KEY_PANEL_GUIDE` - Panel guide
- `KEY_PANEL_INFO` - Panel info
- `KEY_PANEL_TOOLS` - Panel tools

## Usage Examples

### Basic Navigation
```bash
# Navigate through menu
python samsung_remote.py -i 192.168.1.100 -k KEY_MENU
python samsung_remote.py -i 192.168.1.100 -k KEY_UP
python samsung_remote.py -i 192.168.1.100 -k KEY_ENTER
```

### Volume Control
```bash
# Increase volume
python samsung_remote.py -i 192.168.1.100 -k KEY_VOLUP

# Decrease volume
python samsung_remote.py -i 192.168.1.100 -k KEY_VOLDOWN

# Mute
python samsung_remote.py -i 192.168.1.100 -k KEY_MUTE
```

### Power Control
```bash
# Turn off TV
python samsung_remote.py -i 192.168.1.100 -k KEY_POWEROFF

# Turn on TV
python samsung_remote.py -i 192.168.1.100 -k KEY_POWERON
```

### Macro Example
Create a macro file `volume_up.csv`:
```csv
key,wait
KEY_VOLUP,500
KEY_VOLUP,500
KEY_VOLUP,500
```

Execute the macro:
```bash
python samsung_remote.py -i 192.168.1.100 -m volume_up.csv
```

## Notes

1. **Compatibility**: Not all commands work on all Samsung TV models. Newer models support more commands than older ones.

2. **Timing**: Some commands may require specific timing or delays between commands for proper operation.

3. **Model Differences**: Different Samsung TV models may have different command sets or slightly different behavior.

4. **Legacy Mode**: Some older TVs may require using the `-l` (legacy) flag for proper operation.

5. **Network Requirements**: The TV must be on the same network and have network control enabled in the TV settings.

## Troubleshooting

- If commands don't work, try using legacy mode: `-l`
- Ensure the TV's IP address is correct
- Check that network control is enabled on the TV
- Some TVs may require pairing or authentication
- Try different timing between commands in macros

## References

- Samsung TV API documentation
- samsungctl library documentation
- Samsung Smart TV developer documentation
