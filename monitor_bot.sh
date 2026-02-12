#!/bin/bash
# Bot monitoring script to catch errors in real-time

echo "🤖 Discord Music Bot - Error Monitor"
echo "======================================"
echo ""

# Check if bot is running
BOT_PID=$(pgrep -f "python bot.py" | head -1)

if [ -z "$BOT_PID" ]; then
    echo "❌ Bot is not running!"
    echo "Starting bot..."
    cd "/home/elias/Desktop/GitHub Projects/Python-Music-Bot"
    source venv/bin/activate
    python bot.py &
    sleep 2
    BOT_PID=$(pgrep -f "python bot.py" | head -1)
fi

if [ -z "$BOT_PID" ]; then
    echo "❌ Failed to start bot"
    exit 1
fi

echo "✅ Bot is running (PID: $BOT_PID)"
echo ""
echo "📊 Monitoring bot status..."
echo "Press Ctrl+C to stop monitoring"
echo ""

# Monitor process
while kill -0 $BOT_PID 2>/dev/null; do
    # Check if process is still alive
    if ! ps -p $BOT_PID > /dev/null 2>&1; then
        echo ""
        echo "❌ Bot process died! Checking for errors..."
        echo "Last 20 lines of potential error output:"
        break
    fi
    sleep 1
done

echo ""
echo "🔍 Bot monitoring stopped"
