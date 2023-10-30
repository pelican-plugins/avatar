"""Unit testing suite for the Avatar Plugin."""

# Copyright (C) 2015, 2021, 2022  Rafael Laboissiere <rafael@laboissiere.net>
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


import os
from shutil import rmtree
from tempfile import mkdtemp
import unittest

from libgravatar import Gravatar
from libravatar import libravatar_url

from pelican import Pelican
from pelican.settings import read_settings

from . import avatar

GLOBAL_AUTHOR_EMAIL = "homer.simpson@example.com"
ARTICLE_AUTHOR_EMAIL = "bart.simpson@example.com"
GLOBAL_GRAVATAR_URL = Gravatar(GLOBAL_AUTHOR_EMAIL).get_image()
GLOBAL_LIBRVATAR_URL = libravatar_url(GLOBAL_AUTHOR_EMAIL)
ARTICLE_GRAVATAR_URL = Gravatar(ARTICLE_AUTHOR_EMAIL).get_image()
ARTICLE_LIBRAVATAR_URL = libravatar_url(ARTICLE_AUTHOR_EMAIL)


class TestAvatarURL(unittest.TestCase):
    """Class for testing the URL output of the Avatar plugin."""

    def setUp(self, override=None):
        """Set up the test environment."""
        self.output_path = mkdtemp(prefix="pelicantests.")
        self.content_path = mkdtemp(prefix="pelicantests.")
        with open(
            os.path.join(self.content_path, "article_infos.html"), "w"
        ) as article_infos_file:
            article_infos_file.write(
                """
<footer class="post-info">
        <div align="center">
                <img src="{{ article.author_avatar }}">
        </div>
</footer>
"""
            )

        with open(
            os.path.join(self.content_path, "global_info.html"), "w"
        ) as global_infos_file:
            global_infos_file.write(
                """
<footer class="post-info">
        <div align="center">
                <img src="{{ author_avatar }}">
        </div>
</footer>
"""
            )

        settings = {
            "PATH": self.content_path,
            "THEME_TEMPLATES_OVERRIDES": [self.content_path],
            "OUTPUT_PATH": self.output_path,
            "PLUGINS": [avatar],
            "CACHE_CONTENT": False,
            "AVATAR_AUTHOR_EMAIL": GLOBAL_AUTHOR_EMAIL,
        }
        if override:
            settings.update(override)

        with open(
            os.path.join(self.content_path, "global_test.md"), "w"
        ) as test_md_file:
            test_md_file.write("Title: Global Test\nDate: 2019-09-05\n\n")

        with open(os.path.join(self.content_path, "test.md"), "w") as test_md_file:
            test_md_file.write(
                "Title: Test\nDate: 2019-09-05\nEmail: " + ARTICLE_AUTHOR_EMAIL + "\n\n"
            )

        self.settings = read_settings(override=settings)
        pelican = Pelican(settings=self.settings)
        pelican.run()

    def tearDown(self):
        """Tidy up the test environment."""
        rmtree(self.output_path)
        rmtree(self.content_path)

    def _assert_url_in_file(self, filename, url, options):
        with open(os.path.join(self.output_path, filename)) as test_html_file:
            found = False
            search_url = url + options
            for line in test_html_file:
                if search_url in line:
                    found = True
                    break
            assert found

    def test_url(self, options=""):
        """Test whether the Avatar URL appears in the generated HTML file."""
        if self.settings["AVATAR_USE_GRAVATAR"]:
            global_base_url = GLOBAL_GRAVATAR_URL
            article_base_url = ARTICLE_GRAVATAR_URL
        else:
            global_base_url = GLOBAL_LIBRVATAR_URL
            article_base_url = ARTICLE_LIBRAVATAR_URL

        self._assert_url_in_file("test.html", article_base_url, options)
        self._assert_url_in_file("global-test.html", global_base_url, options)


class TestAvatarMissing(TestAvatarURL):
    """Class for testing the "missing picture" option."""

    def setUp(self, override=None):
        """Set up the test environment."""
        self.library = "wavatar"
        TestAvatarURL.setUp(self, override={"AVATAR_MISSING": self.library})

    def test_url(self):
        """Test whether the 'd' option appears in the Avatar URL."""
        TestAvatarURL.test_url(self, r"?d=" + self.library)


class TestAvatarSize(TestAvatarURL):
    """Class for testing the size option."""

    def setUp(self, override=None):
        """Set up the test environment."""
        self.size = 100
        TestAvatarURL.setUp(self, override={"AVATAR_SIZE": self.size})

    def test_url(self):
        """Test whether the 's' option appears in the Avatar URL."""
        TestAvatarURL.test_url(self, r"?s=" + str(self.size))


class TestAvatarUseGravatar(TestAvatarURL):
    """Class for testing the 'use Gravatar' option."""

    def setUp(self, override=None):
        """Set up the test environment."""
        TestAvatarURL.setUp(self, override={"AVATAR_USE_GRAVATAR": True})

    def test_url(self):
        """Test whether Gravatar is used."""
        TestAvatarURL.test_url(self)
