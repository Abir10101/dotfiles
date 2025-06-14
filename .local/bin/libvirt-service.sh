#!/bin/bash

# libvirt Manager Script
# Usage: ./libvirt-manager.sh [enable|disable|status]

set -e

# Handle broken pipe errors properly
set -o pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# libvirt services and sockets
SERVICES=(
    "libvirtd"
    "virtqemud"
    "virtnetworkd"
    "virtnodedevd"
    "virtnwfilterd"
    "virtsecretd"
    "virtstoraged"
    "virtinterfaced"
    "virtlockd"
    "virtlogd"
)

SOCKETS=(
    "libvirtd.socket"
    "libvirtd-ro.socket"
    "libvirtd-admin.socket"
    "virtqemud.socket"
    "virtqemud-ro.socket"
    "virtqemud-admin.socket"
    "virtnetworkd.socket"
    "virtnetworkd-ro.socket"
    "virtnetworkd-admin.socket"
    "virtnodedevd.socket"
    "virtnodedevd-ro.socket"
    "virtnodedevd-admin.socket"
    "virtnwfilterd.socket"
    "virtnwfilterd-ro.socket"
    "virtnwfilterd-admin.socket"
    "virtsecretd.socket"
    "virtsecretd-ro.socket"
    "virtsecretd-admin.socket"
    "virtstoraged.socket"
    "virtstoraged-ro.socket"
    "virtstoraged-admin.socket"
    "virtinterfaced.socket"
    "virtinterfaced-ro.socket"
    "virtinterfaced-admin.socket"
    "virtlockd.socket"
    "virtlockd-admin.socket"
    "virtlogd.socket"
    "virtlogd-admin.socket"
)

# Function to print colored output
print_status() {
    local color=$1
    local message=$2
    echo -e "${color}${message}${NC}"
}

# Function to check if running as root
check_root() {
    if [[ $EUID -ne 0 ]]; then
        print_status $RED "This script must be run as root (use sudo)"
        exit 1
    fi
}

# Function to check if a unit exists
unit_exists() {
    local unit=$1
    systemctl list-unit-files --no-pager --no-legend "${unit}*" | grep -q "^${unit}" 2>/dev/null
}
safe_systemctl() {
    local action=$1
    local unit=$2
    local output
    
    # Capture output and handle broken pipe
    if output=$(systemctl "$action" "$unit" 2>&1); then
        return 0
    else
        local exit_code=$?
        # Check if it's just a broken pipe (exit code 141) or unit not found
        if [[ $exit_code -eq 141 ]]; then
            return 0  # Broken pipe is not a real error for our purposes
        elif echo "$output" | grep -q "not found\|could not be found"; then
            return 1  # Unit doesn't exist
        else
            echo "Error with $unit: $output" >&2
            return $exit_code
        fi
    fi
}

# Function to safely execute systemctl commands
safe_systemctl() {
    local action=$1
    local unit=$2
    local output
    
    # Capture output and handle broken pipe
    if output=$(systemctl "$action" "$unit" --no-pager 2>&1); then
        return 0
    else
        local exit_code=$?
        # Check if it's just a broken pipe (exit code 141) or unit not found
        if [[ $exit_code -eq 141 ]]; then
            return 0  # Broken pipe is not a real error for our purposes
        elif echo "$output" | grep -q "not found\|could not be found"; then
            return 1  # Unit doesn't exist
        else
            echo "Error with $unit: $output" >&2
            return $exit_code
        fi
    fi
}

# Function to enable libvirt
enable_libvirt() {
    print_status $BLUE "Enabling libvirt services and sockets..."
    
    # Unmask services first (in case they were masked)
    print_status $YELLOW "Unmasking services..."
    for service in "${SERVICES[@]}"; do
        if unit_exists "$service"; then
            if safe_systemctl unmask "$service"; then
                print_status $GREEN "✓ Unmasked $service"
            fi
        fi
    done
    
    # Enable and start sockets first
    print_status $YELLOW "Enabling sockets..."
    for socket in "${SOCKETS[@]}"; do
        if unit_exists "$socket"; then
            if safe_systemctl enable "$socket"; then
                print_status $GREEN "✓ Enabled $socket"
            fi
        fi
    done
    
    # Enable services
    print_status $YELLOW "Enabling services..."
    for service in "${SERVICES[@]}"; do
        if unit_exists "$service"; then
            if safe_systemctl enable "$service"; then
                print_status $GREEN "✓ Enabled $service"
            fi
        fi
    done
    
    # Start the main libvirt daemon
    print_status $YELLOW "Starting main libvirt services..."
    if unit_exists "libvirtd"; then
        if safe_systemctl start "libvirtd"; then
            print_status $GREEN "✓ Started libvirtd"
        fi
    elif unit_exists "virtqemud"; then
        if safe_systemctl start "virtqemud"; then
            print_status $GREEN "✓ Started virtqemud"
        fi
    fi
    
    print_status $GREEN "libvirt has been enabled and started!"
}

# Function to disable libvirt
disable_libvirt() {
    print_status $BLUE "Disabling libvirt services and sockets..."
    
    # Stop all services first
    print_status $YELLOW "Stopping services..."
    for service in "${SERVICES[@]}"; do
        if unit_exists "$service"; then
            if safe_systemctl stop "$service"; then
                print_status $GREEN "✓ Stopped $service"
            fi
        fi
    done
    
    # Stop all sockets
    print_status $YELLOW "Stopping sockets..."
    for socket in "${SOCKETS[@]}"; do
        if unit_exists "$socket"; then
            if safe_systemctl stop "$socket"; then
                print_status $GREEN "✓ Stopped $socket"
            fi
        fi
    done
    
    # Disable services
    print_status $YELLOW "Disabling services..."
    for service in "${SERVICES[@]}"; do
        if unit_exists "$service"; then
            if safe_systemctl disable "$service"; then
                print_status $GREEN "✓ Disabled $service"
            fi
        fi
    done
    
    # Disable sockets
    print_status $YELLOW "Disabling sockets..."
    for socket in "${SOCKETS[@]}"; do
        if unit_exists "$socket"; then
            if safe_systemctl disable "$socket"; then
                print_status $GREEN "✓ Disabled $socket"
            fi
        fi
    done
    
    # Mask main services to prevent accidental restart
    print_status $YELLOW "Masking core services..."
    for service in "libvirtd" "virtqemud"; do
        if unit_exists "$service"; then
            if safe_systemctl mask "$service"; then
                print_status $GREEN "✓ Masked $service"
            fi
        fi
    done
    
    print_status $GREEN "libvirt has been completely disabled!"
}

# Function to show status
show_status() {
    # Temporarily disable exit on error for status checks
    set +e
    print_status $BLUE "libvirt Status Report:"
    echo
    
    print_status $YELLOW "Main Services:"
    for service in "libvirtd" "virtqemud"; do
        if unit_exists "$service"; then
            status=$(systemctl is-active "$service" --no-pager 2>/dev/null || echo "inactive")
            enabled=$(systemctl is-enabled "$service" --no-pager 2>/dev/null || echo "disabled")
            
            if [[ "$status" == "active" ]]; then
                color=$GREEN
            else
                color=$RED
            fi
            
            print_status $color "  $service: $status ($enabled)"
        fi
    done
    
    echo
    print_status $YELLOW "Key Sockets:"
    for socket in "libvirtd.socket" "virtqemud.socket"; do
        if unit_exists "$socket"; then
            status=$(systemctl is-active "$socket" --no-pager 2>/dev/null || echo "inactive")
            enabled=$(systemctl is-enabled "$socket" --no-pager 2>/dev/null || echo "disabled")
            
            if [[ "$status" == "active" ]] || [[ "$enabled" == "enabled" ]]; then
                color=$GREEN
            else
                color=$RED
            fi
            
            print_status $color "  $socket: $status ($enabled)"
        fi
    done
    
    echo
    print_status $YELLOW "Network Status:"
    if systemctl is-active virtnetworkd --no-pager >/dev/null 2>&1; then
        print_status $GREEN "  Network daemon: active"
    else
        print_status $RED "  Network daemon: inactive"
    fi
    
    # Check for any active VMs
    if command -v virsh >/dev/null 2>&1; then
        echo
        print_status $YELLOW "Active VMs:"
        if virsh list --state-running 2>/dev/null | grep -q running; then
            virsh list --state-running 2>/dev/null | tail -n +3 | head -n -1
        else
            print_status $RED "  No running VMs"
        fi
    fi
    
    # Re-enable exit on error
    set -e
}

# Function to show usage
show_usage() {
    echo "Usage: $0 [enable|disable|status]"
    echo
    echo "Commands:"
    echo "  enable   - Enable and start all libvirt services"
    echo "  disable  - Stop and disable all libvirt services"
    echo "  status   - Show current status of libvirt services"
    echo
    echo "Examples:"
    echo "  sudo $0 enable"
    echo "  sudo $0 disable"
    echo "  $0 status"
}

# Main script logic
main() {
    case "${1:-}" in
        "enable")
            check_root
            enable_libvirt
            ;;
        "disable")
            check_root
            disable_libvirt
            ;;
        "status")
            show_status
            ;;
        "help"|"-h"|"--help")
            show_usage
            ;;
        *)
            print_status $RED "Invalid or missing command"
            echo
            show_usage
            exit 1
            ;;
    esac
}

# Run main function with all arguments
main "$@"
