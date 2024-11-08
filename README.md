# nice-view-gif
A copy of the nice!view shield from the official ZMK firmware as a ZMK module for the purposes of easily customizing.

If you're looking for the bongo cat code it is in the `bongo-cat` branch.
This module is meant to be used as a tool to send your own gifs to you nice!view. Simply fork this repo and run the python script in the converter directory, and this will edit the files to add a gif to the module.

Replace the url-base and shield name below with whatever you customize in your fork.

## Usage

To use this module, first add it to your config/west.yml by adding a new entry to remotes and projects:

```yml
manifest:
  remotes:
      # zmk official
    - name: zmkfirmware
      url-base: https://github.com/zmkfirmware
    - name: danielsodium                        # your username
      url-base: https://github.com/danielsodium # your github
  projects:
    - name: zmk
      remote: zmkfirmware
      revision: main
      import: app/west.yml
    - name: nice-view-gif                 # your repository name
      remote: danielsodium                # your username
      revision: bongo-cat                 # whatever branch you want
  self:
    path: config
```

Now simply swap out the default nice_view shield on the board for the custom one in your build.yaml file.

```yml
---
include:
  - board: nice_nano_v2
    shield: corne_left nice_view_adapter  nice_view_custom #custom shield
  - board: nice_nano_v2
    shield: corne_right 
```
