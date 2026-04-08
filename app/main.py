# SPDX-FileCopyrightText: 2026 Zoe Nickson <zoe.nickson@sidingsmedia.com>
# SPDX-License-Identifier: MIT

"""
Main server entry point
"""

from fastapi import FastAPI


app = FastAPI()


@app.get("/")
async def root():
    """
    Placeholder for the root API

    Returns:
        Placeholder Message
    """

    return {"message": "Hello world"}
