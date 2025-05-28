import os
import subprocess
import colors

from libqtile import bar, layout, qtile, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen, ScratchPad, DropDown
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from qtile_extras import widget

# Configuration constants
MOD = "mod4"
FONT_FACE = "Cascadia Code Bold"
FONT_SIZE = 14
TERMINAL = guess_terminal()
# CLIPBOARD = "xfce4-popup-clipman"
CLIPBOARD = "/home/abir101/.config/dmenu_scripts/cliphist.sh sel"

# Color scheme setup
colors, backgroundColor, foregroundColor, workspaceColor, chordColor = colors.gruvbox()
accentColor = colors[9]

# Menu configuration
def build_menu_command():
    """Build dmenu command with styling options."""
    return (
        f"dmenu_run"
        f" -fn 'Cascadia Code:size=12:style=Bold'"
        f" -nb '{backgroundColor}'"
        f" -nf '{foregroundColor}'"
        f" -sb '{accentColor[1]}'"
        f" -sf '{foregroundColor}'"
    )

mymenu = build_menu_command()

# Key bindings
keys = [
    # Window focus navigation
    Key([MOD], "j", lazy.layout.next(), desc="Move window focus to other window"),
    Key([MOD], "k", lazy.layout.previous(), desc="Move window focus to other window"),
    
    # Window movement
    Key([MOD, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([MOD, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([MOD, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([MOD, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    
    # Window resizing
    Key([MOD, "control"], "h", lazy.layout.grow_left(), lazy.layout.grow().when(layout=["monadtall"]), desc="Grow window to the left"),
    Key([MOD, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([MOD, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([MOD, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([MOD], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    
    # Layout and window management
    Key([MOD, "shift"], "Return", lazy.layout.toggle_split(), desc="Toggle between split and unsplit sides of stack"),
    Key([MOD], "Return", lazy.spawn(TERMINAL), desc="Launch terminal"),
    Key([MOD], "w", lazy.window.kill(), desc="Kill focused window"),
    
    # Layout switching
    Key([MOD], "m", lazy.to_layout_index(0), desc="Change Layout to Max"),
    Key([MOD], "t", lazy.to_layout_index(1), desc="Change Layout to tile"),
    Key([MOD], "f", lazy.to_layout_index(2), desc="Toggle floating layout"),
    
    # System controls
    Key([MOD, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([MOD, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    
    # Application launchers
    Key([MOD], "d", lazy.spawn(mymenu), desc="Launch app launcher"),
    Key([MOD], "v", lazy.spawn(CLIPBOARD), desc="Launch clipboard manager"),

    # Audio controls
    Key([], "XF86AudioRaiseVolume", lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ +3%"), desc="Raise Volume by 3%"),
    Key([], "XF86AudioLowerVolume", lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ -3%"), desc="Lower Volume by 3%"),
    Key([], "XF86AudioMute", lazy.spawn("pactl set-sink-mute @DEFAULT_SINK@ toggle"), desc="Mute/Unmute Volume"),
]

# Group configuration
GROUP_CONFIG = {
    "names": ["1", "2", "3", "4", "5"],
    "labels": ["1", "2", "3", "4", "5"],
    "layouts": ["monadtall"] * 5
}

def create_groups():
    """Create workspace groups with consistent configuration."""
    groups = []
    for i, name in enumerate(GROUP_CONFIG["names"]):
        groups.append(Group(
            name=name,
            layout=GROUP_CONFIG["layouts"][i].lower(),
            label=GROUP_CONFIG["labels"][i]
        ))
    return groups

groups = create_groups()

# Add group-specific keybindings
for group in groups:
    keys.extend([
        Key([MOD], group.name, lazy.group[group.name].toscreen(), 
            desc="Mod + number to move to that group."),
        Key([MOD, "shift"], group.name, lazy.window.togroup(group.name), 
            desc="Move focused window to new group."),
    ])

# Scratchpad configuration
groups.append(
    ScratchPad("scratchpad", [
        DropDown("volume", "pavucontrol", width=0.5, height=0.6, x=0.25, y=0.1, opacity=1),
    ])
)

# Layout themes and configurations
LAYOUT_THEME = {
    "margin": 0,
    "border_width": 5,
    "border_focus": accentColor,
    "border_normal": backgroundColor
}

FLOATING_THEME = {
    "margin": 0,
    "border_focus": accentColor,
    "border_normal": backgroundColor,
    "border_width": 3,
}

# Define floating layout with rules
floating_layout = layout.Floating(
    **FLOATING_THEME,
    float_rules=[
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),   # gitk
        Match(wm_class="maketag"),      # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),    # gitk
        Match(title="pinentry"),        # GPG key password entry
    ]
)

# Available layouts
layouts = [
    layout.Max(**LAYOUT_THEME),
    layout.MonadTall(**LAYOUT_THEME),
    floating_layout,
]

# Widget factory functions for better organization
def create_separator():
    """Create a consistent separator widget."""
    return widget.TextBox(
        text="┇", 
        fontsize=FONT_SIZE, 
        font=FONT_FACE, 
        background=colors[0], 
        foreground=foregroundColor
    )

def create_text_widget(text, **kwargs):
    """Create a text widget with consistent styling."""
    defaults = {
        "fontsize": FONT_SIZE,
        "font": FONT_FACE,
        "background": colors[0],
        "foreground": foregroundColor
    }
    defaults.update(kwargs)
    return widget.TextBox(text=text, **defaults)

# Widget definitions
separator = create_separator()

open_windows = widget.TaskList(
    highlight_method='block',
    fontsize=FONT_SIZE,
    font=FONT_FACE,
    icon_size=0,
    margin=0,
    padding_y=1,
    rounded=False,
    spacing=0,
    title_width_method='uniform',
    unfocused_border=colors[0],
    border=accentColor,
    foreground=foregroundColor
)

groupbox = widget.GroupBox(
    fontsize=FONT_SIZE,
    font=FONT_FACE,
    padding_x=5,
    rounded=False,
    center_aligned=True,
    disable_drag=True,
    borderwidth=3,
    highlight_method="block",
    active=workspaceColor,
    inactive=foregroundColor,
    highlight_color=colors[0],
    this_current_screen_border=accentColor,
    background=backgroundColor,
    foreground=foregroundColor
)

# System monitoring widgets
cpu_icon = create_text_widget("CPU:")
cpu = widget.CPU(
    font=FONT_FACE, 
    fontsize=FONT_SIZE, 
    format="{load_percent}%", 
    foreground=foregroundColor, 
    background=colors[0]
)

mem_icon = create_text_widget("RAM:")
mem = widget.Memory(
    font=FONT_FACE, 
    fontsize=FONT_SIZE, 
    format="{NotAvailable:.0f}{mm}", 
    background=colors[0], 
    foreground=foregroundColor
)

clock = widget.Clock(
    fontsize=FONT_SIZE, 
    font=FONT_FACE, 
    format="%a %d %b %I:%M", 
    foreground=foregroundColor, 
    background=colors[0]
)

# Volume control widgets
vol_icon = widget.TextBox(
    text="VOL:",
    fontsize=FONT_SIZE,
    font=FONT_FACE,
    background=colors[0],
    foreground=foregroundColor,
    mouse_callbacks={
        "Button1": lazy.group["scratchpad"].dropdown_toggle("volume")
    }
)

vol = widget.Volume(
    fmt="{}",
    mute_command="pamixer -t",
    get_volume_command="pamixer --get-volume-human",
    update_interval=0.3,
    fontsize=FONT_SIZE,
    font=FONT_FACE,
    foreground=foregroundColor,
    background=colors[0]
)

layout_name = widget.CurrentLayout(
    fontsize=FONT_SIZE, 
    font=FONT_FACE, 
    foreground=foregroundColor, 
    background=colors[0]
)

tray = widget.Systray(background=colors[0])

# Screen configuration
screens = [
    Screen(
        top=bar.Bar([
            groupbox,
            open_windows,
            tray,
            separator,
            layout_name,
            separator,
            cpu_icon,
            cpu,
            separator,
            mem_icon,
            mem,
            separator,
            vol_icon,
            vol,
            separator,
            clock,
        ],
        margin=0,
        size=FONT_SIZE + 8,
        background=colors[0]
        ),
        wallpaper="~/.local/share/backgrounds/wall6.png",
        wallpaper_mode="fill"
    ),
]

# Mouse configuration
mouse = [
    Drag([MOD], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([MOD], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([MOD], "Button2", lazy.window.bring_to_front()),
]

# Qtile behavior settings
dgroups_key_binder = None
dgroups_app_rules = []
follow_mouse_focus = False
bring_front_click = False
floats_kept_above = True
cursor_warp = False
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True
auto_minimize = True

# Wayland-specific settings
wl_input_rules = None
wl_xcursor_theme = None
wl_xcursor_size = 24

# Java compatibility
wmname = "LG3D"

# Uncomment to enable autostart script
# @hook.subscribe.startup_once
# def autostart():
#     home = os.path.expanduser('~/.config/qtile/autostart.sh')
#     subprocess.Popen([home])
