#!/usr/bin/env python3
import argparse
from app import TradeBotApp

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='TradeBot - Prädiktiver Handelsbot')
    parser.add_argument('--config', type=str, help='Pfad zur Konfigurationsdatei')
    parser.add_argument('--port', type=int, default=8000, help='Port für den API-Server')

    args = parser.parse_args()

    app = TradeBotApp(config_file=args.config)

    if args.port:
        app.config['api']['port'] = args.port

    try:
        app.start()
    except KeyboardInterrupt:
        print("\nBeende TradeBot...")
        app.stop()