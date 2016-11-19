##Setup
###API Key (Must Have)
[Get an API key from Flickr.](https://www.flickr.com/services/api/misc.api_keys.html) Store in ```~/.flickr_api_key```.

```
echo MY_API_KEY > ~/.flickr_api_key
```

###Install
```
brew install --HEAD  primitive-wallpaper
```

###Start Launch Agent
Launch agent runs ```primitive-wallpaper``` at regular intervals. Output is put in ```~/Pictures/primitive-wallpapers```.

```
brew services start yukunlin/primitive-wallpaper/primitive-wallpaper
```

###Change Desktop Picture
System Preference, Desktop & Screen Saver, add ```~/Pictures/primitive-wallpaper/landscape``` as a folder. If the launch agent is running, new images will be added daily.

##Misc
###Generate Ten 3000px Wide Images
```
primitive-wallpaper -o ~/Pictures/primitive-wallpaper -s 3000 -n 10
```
###Stop Launch Agent
```
brew services stop yukunlin/primitive-wallpaper/primitive-wallpaper
```

##Also see
* https://github.com/fogleman/primitive
