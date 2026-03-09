#!/usr/bin/env python3
"""
Train the plant health prediction model.
"""
import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# Now import from ml-model directory
ml_model_path = Path(__file__).resolve().parent.parent.parent / "ml-model"
sys.path.insert(0, str(ml_model_path))

from train_model import main

if __name__ == "__main__":
    main()
