# .bash_profile

# Get the aliases and functions
if [ -f ~/.bashrc ]; then
    . ~/.bashrc
fi

if [[ -z $DISPLAY ]] && [[ $(tty) == /dev/tty1 ]]; then
    exec dbus-run-session -- qtile start -b wayland
fi

# User specific environment and startup programs
