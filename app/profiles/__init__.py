# SPDX-FileCopyrightText: 2026 Zoe Nickson <zoe.nickson@sidingsmedia.com>
# SPDX-License-Identifier: MIT

"""
User account management

Management of individual user accounts on the system. This does not
include authentication logic, that can be found in auth.
"""

from .views import router  # type: ignore
