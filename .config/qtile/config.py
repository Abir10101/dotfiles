import os
import subprocess
import colors

from libqtile import bar, layout, qtile, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen, ScratchPad, DropDown
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

from qtile_extras import widget


mod = "mod4"
fontFace = "Cascadia Code Bold";
fontSize = 14
terminal = guess_terminal()
clipboard = "xfce4-popup-clipman"

colors, backgroundColor, foregroundColor, workspaceColor, chordColor = colors.gruvbox()
accentColor = colors[9]

mymenu = "dmenu_run"
mymenu += " -fn 'Cascadia Code:size=12:style=Bold'"
mymenu += f" -nb '{backgroundColor}'"
mymenu += f" -nf '{foregroundColor}'"
mymenu += f" -sb '{accentColor[1]}'"
mymenu += f" -sf '{foregroundColor}'"


keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    # Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    # Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    # Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    # Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "j", lazy.layout.next(), desc="Move window focus to other window"),
    Key([mod], "k", lazy.layout.previous(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), lazy.layout.grow().when(layout=["monadtall"]), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([mod], "n", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key([mod], "m", lazy.to_layout_index(0), desc="Change Layout to Max"),
    Key([mod], "t", lazy.to_layout_index(1), desc="Change Layout to tile"),
    # Key(
    #     [mod],
    #     "f",
    #     lazy.window.toggle_fullscreen(),
    #     desc="Toggle fullscreen on the focused window",
    # ),
    # Key([mod], "f", lazy.window.toggle_floating(), desc="Toggle floating on the focused window"),
    Key([mod], "f", lazy.to_layout_index(2), desc="Toggle floating on the focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),

	Key([mod], "d", lazy.spawn(mymenu), desc="Launch app launcher"),
	Key([mod], "v", lazy.spawn(clipboard), desc="Launch clipboard manager"),
	Key([], "XF86AudioRaiseVolume", lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ +3%"), desc="Raise Volume by 3%"),
	Key([], "XF86AudioLowerVolume", lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ -3%"), desc="Lower Volume by 3%"),
	Key([], "XF86AudioMute", lazy.spawn("pactl set-sink-mute @DEFAULT_SINK@ toggle"), desc="Mute/Unmute Volume"),
]

# Add key bindings to switch VTs in Wayland.
# We can't check qtile.core.name in default config as it is loaded before qtile is started
# We therefore defer the check until the key binding is run by using .when(func=...)
# for vt in range(1, 8):
#     keys.append(
#         Key(
#             ["control", "mod1"],
#             f"f{vt}",
#             lazy.core.change_vt(vt).when(func=lambda: qtile.core.name == "wayland"),
#             desc=f"Switch to VT{vt}",
#         )
#     )

groups = []
group_names = ["1", "2", "3", "4", "5"]
group_labels = ["1", "2", "3", "4", "5"]
group_layouts = ["monadtall","monadtall","monadtall","monadtall","monadtall"]
# group_apps = ["st", "LibreWolf", "", "", ""]

# Add group names, labels, and default layouts to the groups object.
for i in range(len(group_names)):
    # groups.append(
    #     Group(
    #         name=group_names[i],
    #         layout=group_layouts[i].lower(),
    #         label=group_labels[i],
    #         matches=Match(title=group_apps[i])
    #     ))
    groups.append(
        Group(
            name=group_names[i],
            layout=group_layouts[i].lower(),
            label=group_labels[i]
        ))


# Add group specific keybindings
for i in groups:
    keys.extend([
        Key([mod], i.name, lazy.group[i.name].toscreen(), desc="Mod + number to move to that group."),
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name), desc="Move focused window to new group."),
    ])


groups.append(
    ScratchPad("scratchpad", [
        DropDown("volume", "pavucontrol", width=0.5, height=0.6, x=0.25, y=0.1, opacity=1),
    ])
)


# Define layouts and layout themes
layout_theme = {
    "margin":0,
    "border_width": 5,
    "border_focus": accentColor,
    "border_normal": backgroundColor
}

floating_layout = layout.Floating(
    margin = 0,
    border_focus = accentColor,
    border_normal = backgroundColor,
    border_width = 3,
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)

layouts = [
    # layout.Columns(**layout_theme),
    layout.Max(**layout_theme),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    layout.MonadTall(**layout_theme),
    # layout.MonadWide(**layout_theme),
    # layout.RatioTile(),
    # layout.Tile(**layout_theme),
    # layout.TreeTab(),
    # layout.VerticalTile(**layout_theme),
    # layout.Zoomy(),
    floating_layout,
]

# widget_defaults = dict(
#     font="Cascadia Code Regular",
#     fontsize=12,
#     padding=3,
# )
# extension_defaults = widget_defaults.copy()

seperator = widget.TextBox(text = "┇", fontsize = fontSize, font = fontFace, background = colors[0], foreground = foregroundColor)
openWindows = widget.TaskList(
                    highlight_method='block',
                    fontsize = fontSize,
                    font = fontFace,
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

groupbox =  widget.GroupBox(
                fontsize = fontSize,
                font = fontFace,
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

cpu = widget.CPU(font=fontFace, fontsize = fontSize, format="{load_percent}%", foreground = foregroundColor, background = colors[0])
cpuicon = widget.TextBox(text = "CPU:", fontsize = fontSize, font = fontFace, background = colors[0], foreground = foregroundColor)

mem = widget.Memory(font=fontFace, fontsize = fontSize, format="{NotAvailable:.0f}{mm}", background=colors[0], foreground=foregroundColor)
memicon = widget.TextBox(text = "RAM:", fontsize = fontSize, font = fontFace, background = colors[0], foreground = foregroundColor)

clock = widget.Clock(fontsize = fontSize, font = fontFace, format="%a %d %b %I:%M", foreground=foregroundColor, background=colors[0])

volicon = widget.TextBox(
        text = "VOL:",
        fontsize = fontSize,
        font = fontFace,
        background = colors[0],
        foreground = foregroundColor,
        mouse_callbacks={
            "Button1": lazy.group["scratchpad"].dropdown_toggle("volume")
        }
    )
vol = widget.Volume(
        fmt="{}",
        mute_command="pamixer -t",
        get_volume_command="pamixer --get-volume-human",
        update_interval=0.3,
        fontsize = fontSize,
        font = fontFace,
        foreground=foregroundColor,
        background=colors[0]
    )

layoutname = widget.CurrentLayout(fontsize = fontSize, font = fontFace, foreground=foregroundColor, background=colors[0])

tray = widget.Systray(background = colors[0])

screens = [
    Screen(
        top=bar.Bar([
            groupbox,
            openWindows,
            tray,
            seperator,
            layoutname,
            seperator,
            cpuicon,
            cpu,
            seperator,
            memicon,
            mem,
            seperator,
            volicon,
            vol,
            seperator,
            clock,
        ],
        margin=0,
        size=fontSize+8,
        background=colors[0]
        ),
        wallpaper = "~/.local/share/backgrounds/wall6.png",
        wallpaper_mode = "fill"
    ),
]


# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = False
bring_front_click = False
floats_kept_above = True
cursor_warp = False

auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# @hook.subscribe.startup_once
# def autostart():
#     home = os.path.expanduser('~/.config/qtile/autostart.sh')
#     subprocess.Popen([home])

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# xcursor theme (string or None) and size (integer) for Wayland backend
wl_xcursor_theme = None
wl_xcursor_size = 24

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
