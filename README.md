# syncthing-activity

This small program uses [Syncthing](https://syncthing.net)'s [REST
API](https://docs.syncthing.net/dev/rest.html) to determine the changes
ocurring on the local instance of Syncthing. (No worries: the API is queried on
the machine on which you run `syncthing-activity`.)

## apikey

Open Syncthing's Web UI at `http://127.0.0.1:8384`, click on _Actions_ and
_Settings_. On the Settings panel, _General_ tab you'll find the API key on the
right. Copy that into an environment variable before launching
`syncthing-activity.py`:

```bash
export SYNCTHING_APIKEY="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
./syncthing-activity.py
```

If your Syncthing is listening on a special URL, you can additionally override
the default URL:

```bash
export SYNCTHING_URL="http://localhost:8384"
```

## usage

Invoking `syncthing-activity` with a regular expression as parameter will cause
it to print lines only if the folder label (the name you gave a syncthing
folder) and the fully qualified path to the item in your file system match that
expression. This makes it possible to view changes on a particular folder only:
the raison d'etre of this program: I wanted to see when a friend who shares a
folder with me added or changed files within that folder.

## example

The program currently outputs the folder label in which an update is detected,
the object (file or directory) and type of update as well as the object's name:


```
      owntracks file  update     platform/ansible/templates/config.f
           take file  update     configs/contacts/mac/.git/index
           take file  metadata   configs/contacts/mac/ab.json
           take file  update     playground/syncthing/events/requirements.txt
           take file  update     playground/syncthing/events/syncthing-activity.py
      on-github file  update     owntracks/recorder/Changelog
           take dir   update     playground/syncthing/events/docs
           take file  delete     playground/syncthing/events/menu
```

(This will change, and I'm open to suggestions.)
