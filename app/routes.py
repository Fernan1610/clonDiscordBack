from flask import Flask, render_template, redirect, url_for, session
from classes.chat import Chat
from classes.country import Country
from classes.user import User
# Redireccionando cuando la página no existe
