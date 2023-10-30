Avatar: A Plugin for Pelican
============================

[![Build Status](https://img.shields.io/github/actions/workflow/status/pelican-plugins/avatar/main.yml?branch=main)](https://github.com/pelican-plugins/avatar/actions)
[![PyPI Version](https://img.shields.io/pypi/v/pelican-avatar)](https://pypi.org/project/pelican-avatar/)
![License](https://img.shields.io/pypi/l/pelican-avatar?color=blue)

This plugin allows the inclusion of [Libravatar][] or [Gravatar][] user profile pictures, corresponding to the email address of the article's author.

[Libravatar]: http://www.libravatar.org
[Gravatar]: http://www.gravatar.com

Installation
------------

This plugin can be installed via:

    python -m pip install pelican-avatar

Usage
-----

### Specifying the Author's Email Address

The default email address is taken from the `AVATAR_AUTHOR_EMAIL` variable in the Pelican settings file. This default value can be overridden on a per-article basis by specifying an email address in the article's metadata:

For reStructuredText:

```rst
:email: bart.simpson@example.com
```

For Markdown:

```markdown
Email: bart.simpson@example.com
```

The plugin first tries to find an avatar image corresponding to the specified email at Libravatar. If it is not found there, the plugin then searches Gravatar. If an avatar for the specified email address is not found at any of those services, a default picture is shown. The default for the "missing picture" can be defined in the configuration variable `AVATAR_MISSING`.

### Adjusting the Template

This plugin assigns the `author_avatar` variable to the avatar image URL and makes that variable available within the article's context. For instance, you can add the following to a template file (for example, to the `article_infos.html` template file), just before the information about the author:

```html
{% if article.author_avatar %}
<div align="center">
        <img src="{{ article.author_avatar }}">
</div>
{% endif %}

```

This will yield the following result (with the [notmyidea][] theme):

![figure](https://github.com/pelican-plugins/avatar/raw/main/avatar-example.png)

[notmyidea]: https://github.com/getpelican/pelican/tree/master/pelican/themes/notmyidea

Page templates work in a similar way:

```html
{% if page.author_avatar %}
<div align="center">
        <img src="{{ page.author_avatar }}">
</div>
{% endif %}
```

To use in common templates, such as `base.html`, you can do something like this:

```html
{% if author_avatar %}
<div align="center">
        <img src="{{ author_avatar }}">
</div>
{% endif %}
```

Or if you want to support optional overriding of the email address in articles or pages, while still using the global configuration if neither is available:

```html
{% if article and article.author_avatar %}
  {% set author_avatar = article.author_avatar %}
{% elif page and page.author_avatar %}
  {% set author_avatar = page.author_avatar %}
{% endif %}
{% if author_avatar %}
<div align="center">
        <img src="{{ author_avatar }}">
</div>
{% endif %}
```

Configuration
-------------

The following variables can be set in the Pelican settings file:

- `AVATAR_AUTHOR_EMAIL`: Site-wide default for the author's email address.

- `AVATAR_MISSING`: The default for the missing picture. This can be either a URL (e.g., `"http://example.com/nobody.png"`) or the name of a library of logos (e.g., `"wavatar"`; for the full set of alternatives, see the [Libravatar API](https://wiki.libravatar.org/api/)).

- `AVATAR_SIZE`: The size, in pixels, of the profile picture (it is always square, so the height is equal to the width). If not specified, the default size (80×80) is returned by Libravatar.

- `AVATAR_USE_GRAVATAR`: The plugin looks up avatars via the Libravatar service by default. Searching the Gravatar service can be forced by setting this configuration variable to `True`.

Credits
-------

Inspiration for this plugin came from the [Gravatar plugin](https://github.com/getpelican/pelican-plugins/tree/master/gravatar).

Contributing
------------

Contributions are welcome and much appreciated. Every little bit helps. You can contribute by improving the documentation, adding missing features, and fixing bugs. You can also help out by reviewing and commenting on [existing issues][].

To start contributing to this plugin, review the [Contributing to Pelican][] documentation, beginning with the **Contributing Code** section.

[existing issues]: https://github.com/pelican-plugins/avatar/issues
[Contributing to Pelican]: https://docs.getpelican.com/en/latest/contribute.html

Acknowledgments
---------------

Thanks to [Justin Mayer][] for helping with migration of this plugin under the Pelican Plugins organization and  to [Troy Curtis][] for adding support for page generator and global generator context and for making improvements in the Poetry workflow.

[Justin Mayer]: https://github.com/justinmayer
[Troy Curtis]: https://github.com/troycurtisjr

Author
------

Copyright (C) 2015, 2021-2023  Rafael Laboissière (<rafael@laboissiere.net>)

License
-------

This project is licensed under the terms of the AGPL 3.0 license.
