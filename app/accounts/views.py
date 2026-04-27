# SPDX-FileCopyrightText: 2026 Zoe Nickson <zoe.nickson@sidingsmedia.com>
# SPDX-License-Identifier: MIT

"""
Endpoints for bank account management operations
"""

import logging

from fastapi import APIRouter

_logger = logging.getLogger(__name__)

_accounts = APIRouter(prefix="/accounts")
_banks = APIRouter(prefix="/banks")

router = APIRouter()
router.include_router(_accounts)
router.include_router(_banks)
