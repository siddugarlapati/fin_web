#!/bin/bash
# Complete training pipeline for Aiza

echo "🚀 Starting Aiza training pipeline..."

# Step 1: Train tokenizer
echo "📝 Training tokenizer..."
python -m scripts.train_tokenizer

# Step 2: Train model
echo "🧠 Training model..."
python -m scripts.train_model

echo "✅ Training complete!"
echo "Start the web interface with: python -m scripts.chat_web"
