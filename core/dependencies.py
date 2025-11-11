# backend/dependencies.py
from .db import SessionLocal
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
import os
import boto3

# Database session dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# AWS S3 client dependency
def get_s3_client():
    s3 = boto3.client(
        "s3",
        region_name=os.getenv("AWS_REGION"),
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
    )
    return s3

