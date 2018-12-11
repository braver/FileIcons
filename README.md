# FileIcons
Colored file icons for Sublime Text. [Also available in greyscale](https://packagecontrol.io/packages/FileIcons%20Mono).

Adds specific, colored icons for most file types for the sidebar in Sublime Text 3. Supports both the Default and Adaptive themes.

<img width="432" src="https://raw.githubusercontent.com/braver/FileIcons/master/icons.png"> 

Inspired by [A File Icon](https://packagecontrol.io/packages/A%20File%20Icon), but simpler:

- Doesn't introduce "alias" languages like "Javascript (Gulpfile)"
- No runtime code: no manipulation of settings or themes, no restarting
- No configuration: just uses existing theme override behavior

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

- Go to the Sublime Text "Packages" directory (e.g. via the command "Browse Packages").
- Download the [latest version](https://github.com/braver/FileIcons/archive/master.zip) of FileIcons, or clone the [repo](https://github.com/braver/FileIcons). [Download](https://github.com/braver/FileIcons/archive/mono.zip) or switch to the [mono](https://github.com/braver/FileIcons/tree/mono) branch for the gray-scale icons.
- Put the "FileIcons" directory you just downloaded/cloned into "Packages" directory.
- In your settings, check what theme you're using (e.g. 'itg.flat.dark.sublime-theme').
- In the FileIcons directory, open the "theme" directory. At the top you should see both "Adaptive.sublime-theme" and "Default.sublime-theme". You can rename either of those to the filename you just found in your settings. 
- Restart Sublime Text and you should see icons in the sidebar!


## Buy me a coffee 

☕️👌🏻

If you enjoy this package, feel free to make a little [donation via PayPal](https://paypal.me/pools/c/8aninMZJ3D) towards the coffee that keeps this project running. It's much appreciated!
