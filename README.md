IP-location Waybar weather plugin
=====================

This fork of the plugin **does not** use the [One Call API from OpenWeatherMap.org](https://openweathermap.org/api/one-call-3).
You **don't** need to have an active subscription, and with normal usage you should never go over the free limit of 1000 request per day.
Instead, you need to obtain a free API-key from [OpenWeatherMap.org](https://home.openweathermap.org/users/sign_up).
My refresh setting for the waybar plugin is 600s.


## set your APIKEY and preferences
You can do this in any way you like. I used env-vars to make life easier (for me). You can absolutely do whatever you want, go ahead and put it right in the code if you prefer doing that, but this is what I would suggest if you are unsure:

In your ~/.bashrc you could add the following definition and place your APIKEY in there

```bash
    # waybar weather settings:
    export WAYBAR_WEATHER_APIKEY="<YOUR OpenWeatherMap API KEY>"                                    # Get one from their website
    export WAYBAR_WEATHER_DEF_POSTAL=<YOUR default zip code>                                        # For when you want another place as fallback
    export WAYBAR_WEATHER_UNITS="metric"                                                            # General units (metric[°C and m/s] / imperial[°F and mph] / metric_simple[° and m/s] / standard[K and m/sec])
    export WAYBAR_WEATHER_ICON_UNITS="metric_simple"                                                # What appears in your waybar (not the tooltip)
```
To make your life even easier, I recommend to set your settings in a sort of "start-script" for both them and waybar. This way you can make sure that they are loaded in the correct place at the correct time (or just do whatever works for you).
I use a .sh file in the following format:

```bash
    # waybar weather settings:
    export WAYBAR_WEATHER_APIKEY="<YOUR OpenWeatherMap API KEY>"                                    
    export WAYBAR_WEATHER_DEF_POSTAL=<YOUR default zip code>                                       
    export WAYBAR_WEATHER_UNITS="metric"
    export WAYBAR_WEATHER_ICON_UNITS="metric_simple"

    exec waybar
```

Which I load in my hyprland config in two ways:
```bash
    exec-once = /home/<username>/.config/waybar/<...>/<name>.sh
    ...                           
    bind = $mainMod, W, exec, killall waybar; /home/<username>/.config/waybar/<...>/<name>.sh
```

If you find this unnecessary, great. At least this will help my future self then.
