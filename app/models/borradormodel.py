from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Date, ForeignKey, DateTime, Boolean, Enum as SAEnum
from sqlalchemy.orm import relationship, declarative_base
from enum import Enum

from app.models.base import Base