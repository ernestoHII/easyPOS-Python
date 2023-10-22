from fastapi import FastAPI, HTTPException, Request, Query, Body, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy import create_engine, desc, Numeric, Column, Integer, String, Float, select
from sqlalchemy import func, over, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base, relationship, joinedload
from sqlalchemy import MetaData, Table
from uvicorn import Config, Server
from typing import List, Optional
import traceback, pyperclip, firebase_admin
from firebase_admin import credentials, firestore
from cryptography.fernet import Fernet
from pydantic import BaseModel
import logging, os, pyodbc
from dotenv import load_dotenv
