# FileIcons Theme

Adds specific icons for most file types for the sidebar in Sublime Text, in both color and monochrome, for any theme.

<img width="432" src="https://raw.githubusercontent.com/braver/FileIcons/master/icons.png"> 

Inspired by [A File Icon](https://packages.sublimetext.com/packages/A%20File%20Icon), and based on [FileIcons](https://packages.sublimetext.com/packages/FileIcons), but now uses the new [file icon theme](https://www.sublimetext.com/docs/themes.html#file-icon-themes) mechanism.


## How to use

Once you've installed the package, add the following to your user preferences:

```json
{
  "file_icon_theme": [
    "FileIcons (mono).sublime-file-icons"
  ],
}
```

For the colored icons replace "mono" with "color". 

By default various configuration file formats are not recognized and matched to their natural file extension. For example `gruntfile.js` will get the icon for JavaScript rather than one specific to Grunt. To enable specific icons for this example and others like `.eslintrc.mjs`, `package.json`, etc. also add the "config" icon theme:


```json
{
  "file_icon_theme": [
    "FileIcons (color).sublime-file-icons",
    "FileIcons config (color).sublime-file-icons"
  ],
}
```

Icons are 18x16 to work well withe Sublime's default themes. To adjust dimensions on any other theme, [customize](https://www.sublimetext.com/docs/themes.html#customization) it by adding this to its `rules`:

```json
{
    "class": "icon_file_type",
    "content_margin": [9, 8]
}
```


## Contributing

The "build" directory contains svg assets. Each icon is assigned a color in icons.json, available colors are listed in colors.json. 

PNG icons are built using a small app written in [Rust](https://www.rust-lang.org).

To add an icon:

- add an svg asset with the correct name
- check that the svg matches the format of the other icons
- add an entry to `build/icons.json` and assign it a color
- add an entry to the preferences directory
- run `make`
- commit the files
- open a PR
- 💃


## Buy me a coffee 

If you enjoy this package, feel free to make a little donation towards the coffee that keeps this project running. It's much appreciated!

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/G2G21VT3Z6)
