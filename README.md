# FileIcons
Colored file icons for Sublime Text. [Also available in greyscale](https://packagecontrol.io/packages/FileIcons%20Mono).

Adds specific, colored icons for most file types for the sidebar in Sublime Text. Supports both the Default and Adaptive themes.

<img width="432" src="https://raw.githubusercontent.com/braver/FileIcons/master/icons.png"> 

Inspired by [A File Icon](https://packagecontrol.io/packages/A%20File%20Icon), but simpler:

- Doesn't introduce "alias" languages like "Javascript (Gulpfile)"
- No runtime code, no restarting required
- Zero configuration

## Customize

The following changes are made to Adaptive/Default.sublime-theme. You can override them by creating a theme file with the same name in your Packages/User directory.

```json
[
  {
    "class": "icon_file_type",
    "layer0.tint": [255, 255, 255],
    "layer0.opacity": 0.75,
    "content_margin": [8, 8]
  },
  {
    "class": "icon_file_type",
    "parents": [{"class": "tree_row", "attributes": ["hover"]}],
    "layer0.opacity": 0.5
  },
  {
    "class": "icon_file_type",
    "parents": [{"class": "tree_row", "attributes": ["selected"]}],
    "layer0.opacity": 1.0
  }
]
```

## Contributing

The "build" directory contains svg assets. Each icon is assigned a color in icons.json, available colors are listed in colors.json. 

To produce png files:

- `npm install`
- `npm run build`

To add an icon:

- add an svg asset with the correct name
- add an entry to icons.json and assign it a color
- add an entry to the preferences directory
- run the build
- commit the files
- open a PR
- 💃

## Enable file icons for 3rd party themes

To get file icons in any theme other than Default or Adaptive, take the following steps:

- After installing [FileIcons](https://packagecontrol.io/packages/FileIcons) through [Package Control](https://packagecontrol.io), go to the Sublime Text "Packages" directory (e.g. via the command "Browse Packages").
- Create a "FileIcons/theme" directory structure in your "Packages" directory.
- In your settings, check what theme you're using (e.g. 'itg.flat.dark.sublime-theme').
- In the "FileIcons/theme" directory, create a file with the name of the theme you are using and copy the [theme overrides](https://github.com/braver/FileIcons/blob/master/theme/Adaptive.sublime-theme) that make FileIcons work into it.
- Restart Sublime Text and you should see icons in the sidebar!


## Buy me a coffee 

☕️👌🏻

If you enjoy this package, feel free to make a little [donation via PayPal](https://paypal.me/koenlageveen) towards the coffee that keeps this project running. It's much appreciated!
