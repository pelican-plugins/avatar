"""Avatar plugin for Pelican."""

# Copyright (C) 2015, 2021-2023  Rafael Laboissière <rafael@laboissiere.net>
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

from libgravatar import Gravatar
from libravatar import libravatar_url

from pelican import signals


def initialize(pelicanobj):
    """Initialize the Avatar plugin."""
    pelicanobj.settings.setdefault("AVATAR_MISSING", None)
    pelicanobj.settings.setdefault("AVATAR_SIZE", None)
    pelicanobj.settings.setdefault("AVATAR_USE_GRAVATAR", None)


def gen_avatar_url(settings, email):
    """Generate the appropriate libravatar/gravatar URL based on the provided email."""
    # Early exit if there is nothing to do
    if not email:
        return None

    missing = settings.get("AVATAR_MISSING")
    size = settings.get("AVATAR_SIZE")

    email = email.lower()
    # Compose URL
    if settings.get("AVATAR_USE_GRAVATAR"):
        url = Gravatar(email).get_image()
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
    return url


def add_avatar_context(generator):
    """Add generator context connector for Avatar plugin."""
    # This adds the avatar URL to the global generator context based on the
    # global setting.
    email = generator.settings.get("AVATAR_AUTHOR_EMAIL")
    url = gen_avatar_url(generator.settings, email)
    if url:
        generator.context["author_avatar"] = url


def add_avatar(generator, metadata):
    """Add Avatar URL to the article/page metadata."""
    # Check the presence of the Email header
    if "email" in metadata:
        email = metadata["email"]
    else:
        email = generator.settings.get("AVATAR_AUTHOR_EMAIL")

    url = gen_avatar_url(generator.settings, email)
    if url:
        # Add URL to the article/page metadata
        metadata["author_avatar"] = url


def register():
    """Register the Avatar plugin with Pelican."""
    signals.initialized.connect(initialize)
    signals.article_generator_context.connect(add_avatar)
    signals.page_generator_context.connect(add_avatar)
    signals.generator_init.connect(add_avatar_context)
