# .bash_profile

# Get the aliases and functions
if [ -f ~/.bashrc ]; then
    . ~/.bashrc
fi

if [[ -z $DISPLAY ]] && [[ $(tty) == /dev/tty1 ]]; then
    dbus-run-session niri --session
    # dbus-run-session mango
fi

# User specific environment and startup programs
