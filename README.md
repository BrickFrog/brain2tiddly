# brain2tiddly

This is more of a personal project for converting notes between "second brain" systems such as Roam/logseq/Obsidian, etc. to TiddlyWiki (TW). The reason for this is that while I like using the aforementioned products for writing/jotting ideas down, I prefer TW as a front-end for display. The annoyance is the differences between files, so I started to write this as a parser that I can run on a cron job as part of the upload schedule for my blog(s).

## (Assumed) FAQ's

* Doesn't TiddlyWiki allow markdown?
  * Yes, but you tend to lose out on a lot of the metadata that makes TW (more) useful.
* Don't a lot of these functions and regex apply only to your specific use case?
  * Yes, at the moment this is highly opinionated (e.g, I use Tags: #Foo, #Bar + espanso for writing the date at the top of a file). Ideally the end goal would be to refactor and extract a lot into config files but I wanted something working to begin with

## Usage?

Assumed usage is simply cloning/downloading the brain2tiddly folder into the folder where one keeps your tiddler + (currently Obsidian) folder since there's a lot of hard coding at the moment. Assumption is your folder is named vault. I just have a make file for building my TW and then call the .py file as part of that process.