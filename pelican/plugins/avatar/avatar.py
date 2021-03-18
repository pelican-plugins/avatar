"""Avatar plugin for Pelican"""

# Copyright (C) 2015, 2021  Rafael Laboissière <rafael@laboissiere.net>
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Affero Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see http://www.gnu.org/licenses/.

from pelican import signals

from libravatar import libravatar_url
from libgravatar import Gravatar


def initialize(pelicanobj):
    """Initialize the Avatar plugin"""
    pelicanobj.settings.setdefault("AVATAR_MISSING", None)
    pelicanobj.settings.setdefault("AVATAR_SIZE", None)
    pelicanobj.settings.setdefault("AVATAR_USE_GRAVATAR", None)


def add_avatar(generator, metadata):
    """Article generator connector for the Avatar plugin"""
    missing = generator.settings.get("AVATAR_MISSING")
    size = generator.settings.get("AVATAR_SIZE")

    # Check the presence of the Email header
    if "email" in metadata.keys():
        email = metadata["email"]
    else:
        email = generator.settings.get("AUTHOR_EMAIL")

    # Add the Libravatar URL
    if email:

        # Lowercase email address
        email = email.lower()

        # Compose URL
        if generator.settings.get("AVATAR_USE_GRAVATAR"):
            url = Gravatar(email).get_profile()
        else:
            url = libravatar_url(email)

        # Add eventual "missing picture" option
        if missing or size:
            url = url + "?"
            if missing:
                url = url + "d=" + missing
                if size:
                    url = url + "&"
            if size:
                url = url + "s=" + str(size)

        # Add URL to the article's metadata
        metadata["author_avatar"] = url


def register():
    """Register the Avatar plugin with Pelican"""
    signals.initialized.connect(initialize)
    signals.article_generator_context.connect(add_avatar)
