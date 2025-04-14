#!/usr/bin/env python3
"""
generate_uuid.py
Generate a UUID4 string using the uuid module.
This script demonstrates how to generate a UUID4 string using the uuid module in Python.
"""
import uuid

def generate_uuid():
    """
    Generate a UUID4 string.
    Returns:
        str: A randomly generated UUID4 string.
    """
    return str(uuid.uuid4())


if __name__ == "__main__":
    print(f"Generated UUID: {generate_uuid()}")

    print("\nMultiple UUIDs:")
    for i in range(5):
        print(f"{i+1}. {generate_uuid()}")
