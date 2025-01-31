# ntfysender
# Copyright (C) 2025 Alexelgt

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from typing import Optional

import base64

import json
import requests


class NtfySender:
    """Class to send messages to a NTFY server"""

    def __init__(
        self,
        server_url: str,
        default_topic: str,
        ntfy_user: Optional[str] = None,
        ntfy_password: Optional[str] = None,
    ) -> None:
        """Initialize and instance of the class

        Args:
            server_url (str): NTFY server URL
            default_topic (str): default topic to use when a message is sent
            ntfy_user (str, optional): NTFY user for Basic authentication. Defaults to None
            ntfy_password (str, optional): NTFY password for Basic authentication. Defaults to None
        """
        self.server_url = server_url
        self.default_topic = default_topic
        self.__set_auth(ntfy_user, ntfy_password)
        self.__set_header()

    def __set_auth(
        self,
        ntfy_user: Optional[str] = None,
        ntfy_password: Optional[str] = None,
    ) -> None:
        """Set authentication for the requests sent to the NFTY server

        Args:
            ntfy_user (str, optional): NTFY user for Basic authentication. Defaults to None
            ntfy_password (str, optional): NTFY password for Basic authentication. Defaults to None
        """
        if ntfy_user is None or ntfy_password is None:
            self._auth = None
        else:
            self._auth = "Basic " + base64.b64encode(f"{ntfy_user}:{ntfy_password}".encode()).decode()

    def __set_header(self):
        """Set base headers dict to use for the requests sent to the NFTY server.

        If the authentication is set, then it is included in the header
        """
        self.headers = {}

        if self._auth is not None:
            self.headers["Authorization"] = self._auth

    def send_msg(
        self,
        title: str,
        message: str,
        link_url: Optional[str] = None,
        topic: Optional[str] = None,
        tags: Optional[str] = None,
        icon: Optional[str] = None,
        timeout: int = 10
    ) -> None:
        """Send a notification message

        Args:
            title (str): Title of the message
            message (str): Body of the message
            link_url (str, optional): URL to open when the notification is pressed. Defaults to None
            topic (str, optional): topic to send the message. If None then self.default_topic is used. Defaults to None
            tags (str, optional): tags to include in the title. Defaults to None
            icon (str, optional): message icon to show. Defaults to None
            timeout (int, optional): time in seconds to wait. Defaults to 10
        """
        topic_send = self.default_topic if topic is None else topic

        self.headers["Title"] = title
        self.headers["Click"] = link_url

        if tags is not None:
            self.headers["Tags"] = tags

        if icon is not None:
            self.headers["Icon"] = icon

        requests.post(
            url=self.server_url,
            headers=self.headers,
            data=json.dumps({
                "topic": topic_send,
                "message": message
            }),
            timeout=timeout
        )
