import os
import argparse
import json
import logging
import time
import uuid
import waitress
from flask import Flask, send_from_directory, jsonify, request
from flask_cors import CORS

from .bridge import BridgeAPI
from ..core.robonaldo import Robonaldo
from .. import config

static = os.path.dirname(__file__) + "/static/"
log = logging.getLogger("robonaldo-webui")


def initialize(robonaldo: Robonaldo):
    global bridge
    bridge = BridgeAPI(robonaldo)
    logging.getLogger("waitress").name = "robonaldo-webui"


def serve():
    global bridge

    ip: str = config.cfg["webui.ip"]
    port: str = config.cfg["webui.port"]

    app = Flask("Robonaldo WebUI", static_folder=static)
    CORS(app)

    @app.get("/bridge")
    def bridge():
        try:
            data = bridge._handle_request()
            if data is False:
                data = {
                    "code": 404,
                    "message": "Command not found.",
                    "data": "https://http.cat/404.jpg",
                }
            if data is True:
                data = {
                    "code": 400,
                    "message": "Invalid request arguments.",
                    "data": "https://http.cat/400.jpg",
                }
        except Exception as e:
            error_id = str(uuid.uuid4())

            log.error(
                "Error happened when trying to handle request. (ID: " + error_id + ")"
            )
            log.error(e)

            data = {
                "code": 500,
                "message": "Internal server error, please see server logs.",
                "error_id": error_id,
                "data": "https://http.cat/500.jpg",
            }

        return jsonify(data)

    @app.get("/")
    def main():  # pylint: disable=unused-variable
        return send_from_directory(static, "index.html")

    waitress.serve(app, listen="%s:%s" % (ip, port), threads=2)
