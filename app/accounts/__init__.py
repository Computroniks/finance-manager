# SPDX-FileCopyrightText: 2026 Zoe Nickson <zoe.nickson@sidingsmedia.com>
# SPDX-License-Identifier: MIT

"""
Bank account management.

Accounts let you manage your bank accounts, open and closed, see their
value over time and store related documents such as statements. Interest
accrued on certain account types will be included in tax calculations.
"""

from .views import router  # type: ignore
