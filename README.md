# shortcore-py

There comes a time in a developer's life when they need to programmatically
post links to dashboards or metrics or whatever to a chat channel and if
said links happen to be aboout 96 characters long they might feel the need
to shorten that to, say, 25 (or much less with a shorter hostname).

Of course a self-hosted url shortener service would be a solution, so that's
what the developer set out to write in a few hours' time only to recognize
that said service had already [been written 5 years ago][sc] in a different
language. So the name and part of the readme will be adapted.

## Installation
* git checkout
* use the provided urls.sqlite-dist or create your own:
```
CREATE TABLE urls (key TEXT, url TEXT, counter INT, created DATE, PRIMARY KEY(key));
```
* Prepare & run
```
pip install flask
python shortcore.py
```

[sc]: https://github.com/winks/shortcore
