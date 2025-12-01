#!/bin/bash
# Complete training pipeline for Aiza Finance AI

echo "======================================"
echo "Aiza Finance AI - Complete Training"
echo "======================================"
echo ""

# Step 1: Generate training data
echo "Step 1: Generating finance training data..."
python -m scripts.generate_finance_data
if [ $? -ne 0 ]; then
    echo "❌ Failed to generate training data"
    exit 1
fi
echo "✓ Training data generated"
echo ""

# Step 2: Train tokenizer (if needed)
if [ ! -f "tokenizer.json" ]; then
    echo "Step 2: Training tokenizer..."
    python -m scripts.train_tokenizer
    if [ $? -ne 0 ]; then
        echo "⚠️  Tokenizer training failed, will use default"
    else
        echo "✓ Tokenizer trained"
    fi
else
    echo "Step 2: Tokenizer already exists, skipping..."
fi
echo ""

# Step 3: Train model
echo "Step 3: Training finance model..."
python -m scripts.train_finance_model
if [ $? -ne 0 ]; then
    echo "❌ Model training failed"
    exit 1
fi
echo "✓ Model trained"
echo ""

# Step 4: Evaluate model
echo "Step 4: Evaluating model performance..."
python -m scripts.evaluate_model
if [ $? -ne 0 ]; then
    echo "⚠️  Evaluation failed, but model is trained"
else
    echo "✓ Evaluation complete"
fi
echo ""

# Done
echo "======================================"
echo "✓ Training Complete!"
echo "======================================"
echo ""
echo "Your Aiza finance AI is ready!"
echo ""
echo "To start the web interface:"
echo "  python -m scripts.chat_web"
echo ""
echo "Then visit: http://localhost:8000"
echo ""
