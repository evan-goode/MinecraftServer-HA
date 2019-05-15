# Minecraft Server Home Assistant Sensor
"Monitor your Minecraft server or flash your living room lights when someone joins your Minecraft server!"

![Screenshot](screenshot.PNG)

Add `minecraft.py` and `manifest.json` to your `custom_components/minecraft` folder and use this in your config:

```
sensor:
  platform: minecraft
  name: [NAME]
  server: [SERVER_ADDRESS]
```
In your Minecraft Server configuration file, set query=true. Failure to do so will cause communication errors.
