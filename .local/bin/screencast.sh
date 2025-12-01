#!/bin/bash

# screencast - Manage screen sharing portals
# Usage: screencast [--start|--stop|--status]

start_portals() {
    if pgrep -x "xdg-desktop-por" > /dev/null; then
        echo "✓ Portals are already running"
        return 0
    fi
    
    echo "Starting screen sharing portals..."
    /usr/libexec/xdg-desktop-portal-wlr > /dev/null 2>&1 &
    sleep 1
    /usr/libexec/xdg-desktop-portal > /dev/null 2>&1 &
    sleep 1
    
    if pgrep -x "xdg-desktop-por" > /dev/null; then
        echo "✓ Portals started successfully"
    else
        echo "✗ Failed to start portals"
        return 1
    fi
}

stop_portals() {
    if ! pgrep -x "xdg-desktop-por" > /dev/null; then
        echo "✓ Portals are not running"
        return 0
    fi
    
    echo "Stopping screen sharing portals..."
    pkill -f xdg-desktop-portal-wlr
    pkill -f xdg-desktop-portal
    sleep 1
    
    if ! pgrep -x "xdg-desktop-por" > /dev/null; then
        echo "✓ Portals stopped successfully"
    else
        echo "✗ Failed to stop portals"
        return 1
    fi
}

show_status() {
    echo "Portal Status:"
    echo "─────────────────────────────────────"
    
    if pgrep -f "xdg-desktop-portal-wlr" > /dev/null; then
        echo "xdg-desktop-portal-wlr: ✓ Running (PID: $(pgrep -f xdg-desktop-portal-wlr))"
    else
        echo "xdg-desktop-portal-wlr: ✗ Stopped"
    fi
    
    if pgrep -x "xdg-desktop-por" > /dev/null; then
        echo "xdg-desktop-portal:     ✓ Running (PID: $(pgrep -x xdg-desktop-por))"
    else
        echo "xdg-desktop-portal:     ✗ Stopped"
    fi
}

show_help() {
    cat << EOF
Usage: screencast [OPTION]

Manage screen sharing portals for Wayland

Options:
  --start     Start xdg-desktop-portal services
  --stop      Stop xdg-desktop-portal services
  --status    Show current portal status
  --help      Show this help message

Examples:
  screencast --start
  screencast --stop
  screencast --status
EOF
}

# Main script logic
case "$1" in
    --start)
        start_portals
        ;;
    --stop)
        stop_portals
        ;;
    --status)
        show_status
        ;;
    --help|"")
        show_help
        ;;
    *)
        echo "Error: Unknown option '$1'"
        echo "Use 'screencast --help' for usage information"
        exit 1
        ;;
esac
