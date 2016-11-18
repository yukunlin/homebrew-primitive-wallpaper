##Setup
###API Key (Must Have)
[Get an API key from Flickr.](https://www.flickr.com/services/api/misc.api_keys.html) Store in ```~/.flickr_api_key```.

```
echo MY_API_KEY > ~/.flickr_api_key
```

###Install
```
brew install --HEAD  primitive-wallpaper --with-launchd
```

###Start Launch Agent
Launch agent runs ```primitive-wallpaper``` every 6 hours to generate a wallpaper. Puts it in ```~/Pictures/primitive-wallpapers```.

```
brew services start yukunlin/primitive-wallpaper/primitive-wallpaper
```

##Misc
###Generate Ten 3000px Wide Images
```
primitive-wallpaper -o ~/Pictures/primitive-wallpapers -s 3000 -n 10
```
###Stop Launch Agent
```
brew services stop yukunlin/primitive-wallpaper/primitive-wallpaper
```
