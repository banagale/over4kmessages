# over4kmessages

This is a test project to demo Django's behavior when large amounts of data are passed through the `messages`
application.

## Why

[Episode 15](https://djangoriffs.com/episodes/user-session-data) of [Django Riffs](https://djangoriffs.com/) podcast
focuses on auth, which includes a detailed look at `session`.

Toward the end of the episode, Matt Layman ([@mblayman](https://twitter.com/mblayman)) mentions a limit on the size of
cookies and asks listeners to report what happens if too much message data is passed through.

## How this test project works

In `settings.py` sets the `MESSAGE_STORAGE` setting to cookie storage, then the main view takes a trivial form POST and
includes a very long string of text.

The `contacts.const.py` file contains increasingly large strings that are duplications of Charles Bukowski's poem,
"[Style](https://www.goodreads.com/quotes/150224-style-is-the-answer-to-everything-a-fresh-way-to)" These were created
using [this online text size calculator](http://bytesizematters.com/) and verified by saving on disk.

The `contacts.views.py`
file [contains an easy way](https://github.com/banagale/over4kmessages/blob/main/contacts/views.py#L17) to toggle use
any of these text blobs to `messages`. The project is by default set to use the 166 kb text.

## Result

Increasingly large text blocks well beyond the believed 4k max were still allowed to pass through the cookie storage.

However, somewhere between 72kb and 166kb is too much text.

When the 166kb of text is passed as the message in `contacts.views` Django throws an exception:

> Not all temporary messages could be stored.

This occurs in `django.contrib.messages.middleware.py`

<img width="488" alt="too large of a messages message error" src="https://user-images.githubusercontent.com/1409710/133337136-28445bb6-f6c5-44a4-b0cf-c1f317933f66.png">

## Digging

It turns out django limits the max cookie size to 2048,
in [django.contrib.messages.storage.cooky.CookieStorage](https://github.com/django/django/blob/main/django/contrib/messages/storage/cookie.py#L70)
.

A comment in the code point out a decade old Django ticket [#18781](https://code.djangoproject.com/ticket/18781) which
details a need to reduce the max cookie size from what was then 3072 created by django to make room for large headers.

This doesn't explain why 72kb+ sized message would make it through a cookie. Perhaps, compression is involved here!

Searching `contrib.messages.storage.cookie.py` for 'compress' yields the `_encode()` method which passes `message`
along and a `compress=True` argument to `django.core.signing.Signer.sign_object`

`sign_object()` [has a conditional](https://github.com/django/django/blob/ec212c66167759a2a40b13d5efc47d883816d4da/django/core/signing.py#L189)
for `compress` that shows the python standard
library, [`zlib`](https://docs.python.org/3/library/zlib.html#zlib.compress) is being used.

That is what is allowing these larger messages to make it through.

## New questions

- What is the true max text size that can be compressed using `zlib.compress()` to duck the 2048 threshold for cookie
  storage?
- Should django still be using `zlib.compress()` to pack data into cookies?
- Really, if we're passing a long a message to our user on page load, should it be longer than 140 chars anyway?
  (Probably not but that's the opposite of the point of all of this!)

## References for more on compression

- Writing a custom compression method to outperform `zlib.compress()`:
  [Don Cross](https://github.com/cosinekitty)
  , [Winning the Data Compression Game](https://towardsdatascience.com/winning-the-data-compression-game-af145363ae49)
- Question related to improving on `zlib.compress()`:
  Stack
  Overflow, [zlib compress() produces awful compression rate](https://stackoverflow.com/questions/27107492/zlib-compress-produces-awful-compression-rate)
