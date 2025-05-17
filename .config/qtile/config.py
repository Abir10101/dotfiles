import os
import subprocess
import colors

from libqtile import bar, layout, qtile, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen, ScratchPad, DropDown
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

from qtile_extras import widget
# from qtile_extras.widget.decorations import PowerLineDecoration
from qtile_extras.widget import decorations
from qtile_extras.widget.decorations import RectDecoration



mod = "mod4"
terminal = guess_terminal()
mymenu = "dmenu_run -fn 'Cascadia Code-10'"
clipboard = "xfce4-popup-clipman"

colors, backgroundColor, foregroundColor, workspaceColor, chordColor = colors.gruvbox()


right_hand1 = {
    "decorations": [
        RectDecoration(colour=colors[11], radius=[0, 4, 4, 0], filled=True, padding_y=0, padding_x=0)
    ],
    "padding": 10,
}


left_hand1 = {
    "decorations": [
        RectDecoration(colour=colors[6], radius=[4, 0, 0, 4], filled=True, padding_y=0, group=True)
    ],
    "padding": 10,
}

left_hand2 = {
    "decorations": [
        RectDecoration(colour=colors[4], radius=[4, 0, 0, 4], filled=True, padding_y=0, group=True)
    ],
    "padding": 10,
}

left_hand3 = {
    "decorations": [
        RectDecoration(colour=colors[5], radius=[4, 0, 0, 4], filled=True, padding_y=0, group=True)
    ],
    "padding": 10,
}


left_hand4 = {
    "decorations": [
        RectDecoration(colour=colors[7], radius=[4, 0, 0, 4], filled=True, padding_y=0, group=True)
    ],
    "padding": 10,
}

left_hand5 = {
    "decorations": [
        RectDecoration(colour=colors[8], radius=[4, 0, 0, 4], filled=True, padding_y=0, group=True)
    ],
    "padding": 10,
}

left_hand6 = {
    "decorations": [
        RectDecoration(colour=colors[3], radius=[4, 0, 0, 4], filled=True, padding_y=0, group=True)
    ],
    "padding": 10,
}


def open_launcher():
    qtile.spawn(mymenu)



keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key(["mod1"], "tab", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
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
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key(
        [mod],
        "f",
        lazy.window.toggle_fullscreen(),
        desc="Toggle fullscreen on the focused window",
    ),
    Key([mod], "t", lazy.window.toggle_floating(), desc="Toggle floating on the focused window"),
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
group_names = ["1", "2", "3", "4", "5", "6"]
group_labels = ["1", "2", "3", "4", "5", "6"]
group_layouts = ["columns","columns","columns","columns","columns","columns"]

# Add group names, labels, and default layouts to the groups object.
for i in range(len(group_names)):
    groups.append(
        Group(
            name=group_names[i],
            layout=group_layouts[i].lower(),
            label=group_labels[i],
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
        "margin":2,
        "border_width": 3,
        "border_focus": colors[6],
        "border_normal": colors[2]
    }

layouts = [
    layout.Columns(**layout_theme),
    layout.Max(**layout_theme),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font="Cascadia Code Regular",
    fontsize=12,
    padding=3,
)
extension_defaults = widget_defaults.copy()


logo = widget.TextBox(text="π", font="Cascadia Code", mouse_callbacks={"Button1": open_launcher}, fontsize=15, background=colors[4], margin=2, padding=7)
spacer1 = widget.Spacer(length=1, background=colors[4])
spacer3 = widget.Spacer(background=colors[0])
spacer4 = widget.Spacer(length=4, background=colors[0])
groupbox =  widget.GroupBox(
                font="Cascadia Mono",
                fontsize=12,
                padding_x=5,
                padding_y=5,
                rounded=False,
                center_aligned=True,
                disable_drag=True,
                borderwidth=3,
                highlight_method="line",
                hide_unused = True,
                active=colors[6],
                inactive=colors[1],
                highlight_color=colors[0],
                this_current_screen_border=colors[3],
                this_screen_border=colors[7],
                other_screen_border=colors[4],
                other_current_screen_border=colors[3],
                background=colors[0],
                foreground=colors[3],
            )
cpu = widget.CPU(font="Cascadia Code", format="{load_percent}%", foreground=colors[2], background=colors[0], **right_hand1)
cpuicon = widget.TextBox(text = "", fontsize = 20, font = "Cascadia Mono", background = colors[0], foreground = colors[0], **left_hand1)

mem = widget.Memory(font="Cascadia Code", format="{MemUsed:.0f}{mm}", background=colors[0], foreground=colors[2], **right_hand1)
memicon = widget.TextBox(text = "󰈀", fontsize = 20, font = "Cascadia Mono", background = colors[0], foreground = colors[0], **left_hand3)

clockicon = widget.TextBox(text = "", fontsize = 20, font = "Cascadia Mono", background = colors[0], foreground = colors[0], **left_hand4)
clock = widget.Clock(font="Cascadia Code", format="%a %d %b %I:%M", foreground=colors[2], background=colors[0], **right_hand1)

volicon = widget.TextBox(
        text = "󰕾",
        fontsize = 20,
        font = "Cascadia Mono",
        background = colors[0],
        foreground = colors[0],
        mouse_callbacks={
            "Button1": lazy.group["scratchpad"].dropdown_toggle("volume")
        },
        **left_hand5
    )
vol = widget.Volume(
        fmt="{}",
        mute_command="pamixer -t",
        get_volume_command="pamixer --get-volume-human",
        update_interval=0.3,
        font="Cascadia Code",
        foreground=colors[2],
        background=colors[0],
        **right_hand1
    )

curlayout= widget.CurrentLayoutIcon(scale=0.65, background = colors[0], **left_hand6)
layoutname = widget.CurrentLayout(font = "Cascadia Code", foreground=colors[2], background=colors[0], **right_hand1)

tray = widget.Systray(background = colors[0])

screens = [
    Screen(
        top=bar.Bar([
            logo,
            spacer1,
            groupbox,
            spacer3,
            curlayout,
            layoutname,
            spacer4,
            cpuicon,
            cpu,
            spacer4,
            memicon,
            mem,
            spacer4,
            clockicon,
            clock,
            spacer4,
            volicon,
            vol,
            spacer4,
            tray,
            spacer4,
            ],
            margin=0,
            size=18
        ),
        wallpaper = "~/.local/share/backgrounds/wallpaper.jpg",
        wallpaper_mode = "fill"
    ),
]

# screens = [
#     Screen(
#         top=bar.Bar(
#             [
#                 widget.CurrentLayout(),
#                 widget.GroupBox(),
#                 widget.Prompt(),
#                 widget.WindowName(),
#                 widget.Chord(
#                     chords_colors={
#                         "launch": ("#ff0000", "#ffffff"),
#                     },
#                     name_transform=lambda name: name.upper(),
#                 ),
#                 widget.TextBox("default config", name="default"),
#                 widget.TextBox("Press &lt;M-r&gt; to spawn", foreground="#d75f5f"),
#                 # NB Systray is incompatible with Wayland, consider using StatusNotifier instead
#                 # widget.StatusNotifier(),
#                 widget.Systray(),
#                 widget.Clock(format="%Y-%m-%d %a %I:%M %p"),
#                 widget.QuickExit(),
#             ],
#             24,
#             # border_width=[2, 0, 2, 0],  # Draw top and bottom borders
#             # border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
#         ),
#         # You can uncomment this variable if you see that on X11 floating resize/moving is laggy
#         # By default we handle these events delayed to already improve performance, however your system might still be struggling
#         # This variable is set to None (no cap) by default, but you can set it to 60 to indicate that you limit it to 60 events per second
#         # x11_drag_polling_rate = 60,
#         wallpaper = "~/.local/share/backgrounds/wallpaper.jpg",
#         wallpaper_mode = "fill",
#     ),
# ]

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
floating_layout = layout.Floating(
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
