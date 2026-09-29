#!/bin/bash
echo "======================================================================"
echo "   AI-Powered Environmental Intelligence System"
echo "   Air Quality Prediction & Smart Mobility Recommendations"
echo "======================================================================"
echo ""

if [ -f "venv/bin/python" ]; then
    PYTHON_CMD="venv/bin/python"
else
    PYTHON_CMD="python3"
fi

echo "[1/3] Checking environment..."
$PYTHON_CMD -c "import fastapi, uvicorn, sklearn, pandas, joblib; print('Dependencies verified.')" 2>/dev/null || {
    echo "[!] Installing dependencies..."
    pip install fastapi uvicorn pandas joblib scikit-learn requests
}

echo ""
echo "[2/3] Launching FastAPI Backend on http://127.0.0.1:8000 ..."
echo ""

if which xdg-open > /dev/null; then
    (sleep 2 && xdg-open http://127.0.0.1:8000) &
elif which open > /dev/null; then
    (sleep 2 && open http://127.0.0.1:8000) &
fi

$PYTHON_CMD -m uvicorn backend.app:app --host 127.0.0.1 --port 8000 --reload
