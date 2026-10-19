import json
import time
import random
import threading
from flask import Blueprint, Flask, jsonify, render_template, request, redirect, url_for, sessio
from datetime import date, timedelta, datetime
bombu = Blueprint('bombu', __name__)


