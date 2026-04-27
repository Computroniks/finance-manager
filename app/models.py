# SPDX-FileCopyrightText: 2026 Zoe Nickson <zoe.nickson@sidingsmedia.com>
# SPDX-License-Identifier: MIT

"""
Codebase wide models
"""

from pydantic import BaseModel


class HttpError(BaseModel):
    """General error response"""

    detail: str
