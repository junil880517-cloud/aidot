#!/bin/bash
# ===========================================
# DOT System - Service Manager
# ===========================================

INSTALL_DIR="$HOME/dot-project"

if [ ! -d "$INSTALL_DIR" ]; then
    echo "[ERROR] DOT system is not installed."
    echo "        Expected: $INSTALL_DIR"
    exit 1
fi

cd "$INSTALL_DIR"

case "$1" in
    start)
        echo "Starting DOT services..."
        docker compose up -d
        echo "Done."
        ;;
    stop)
        echo "Stopping DOT services..."
        docker compose down
        echo "Done."
        ;;
    restart)
        echo "Restarting DOT services..."
        docker compose down
        docker compose up -d
        echo "Done."
        ;;
    status)
        docker compose ps
        ;;
    logs)
        docker compose logs -f ${2:-}
        ;;
    *)
        echo "DOT System - Service Manager"
        echo ""
        echo "Usage: $0 {start|stop|restart|status|logs}"
        echo ""
        echo "  start    - Start all services"
        echo "  stop     - Stop all services"
        echo "  restart  - Restart all services (reload .env)"
        echo "  status   - Show service status"
        echo "  logs     - Show logs (optional: service name)"
        echo ""
        echo "Examples:"
        echo "  $0 start"
        echo "  $0 logs backend"
        ;;
esac
