import json
import time
import random
import threading
from flask import Flask, jsonify, render_template, request, redirect, url_for, session
from kanji_no_sekai_memokanji import *
from kanji_no_sekai_paper import *
from datetime import date, timedelta, datetime




