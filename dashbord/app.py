\-- dashboard/app.py --
import os
import time
import logging
from pyspark.sql import SparkSession
import dash
from dash import dcc, html
from dash.dependencies import Input,Output
import dash\_bootstrap\_components as dbc
import plotly.express as px

logging.basicConfig(level=logging.INFO)
app=dash.Dash(**name**,external\_stylesheets=\[dbc.themes.BOOTSTRAP])
spark=SparkSession.builder.master(os.getenv('SPARK\_MASTER')).appName('dash').getOrCreate()
server=app.server
... (rest of dashboard.py)
