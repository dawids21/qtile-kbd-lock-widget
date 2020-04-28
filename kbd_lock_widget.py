import os
from libqtile.widget import base
from libqtile import bar
from libqtile.images import Img


class KbdLockWidget(base._Widget, base.MarginMixin):
    """Lock keyboard with mouse click"""
    orientations = base.ORIENTATION_BOTH
    defaults = [
        ("scale", True, "Enable/Disable image scaling"),
        ("rotate", 0.0, "rotate the image in degrees counter-clockwise"),
        ("lock_icon", None, "Lock icon filename. Can contain '~'"),
        ("unlock_icon", None, "Unlock icon filename. Can contain '~'"),
        ("keyboard_device_id", 0, "Keyboard id. Obtainable by xinput list"),
        ("keyboard_master_id", 0, "Keyboard master id. Obtainable by xinput list"),
    ]
    def __init__(self, length=bar.CALCULATED, **config):

        base._Widget.__init__(self, length, **config)
        self.add_defaults(KbdLockWidget.defaults)
        self.add_defaults(base.MarginMixin.defaults)

        # make the default 0 instead
        self._variable_defaults["margin"] = 0

        # at the start keyboard is unlocked
        self.is_locked = False

    def _configure(self, qtile, bar):
        base._Widget._configure(self, qtile, bar)

        if not self.lock_icon or not self.unlock_icon:
            raise ValueError("Icons not set!")

        self.lock_icon = os.path.expanduser(self.lock_icon)
        self.unlock_icon = os.path.expanduser(self.unlock_icon)

        if not os.path.exists(self.lock_icon):
            raise ValueError("File does not exist: {}".format(self.lock_icon))
        if not os.path.exists(self.unlock_icon):
            raise ValueError(
                "File does not exist: {}".format(self.unlock_icon))

        self.img_lock = Img.from_path(self.lock_icon)
        self.img_unlock = Img.from_path(self.unlock_icon)
        self.img_lock.theta = self.rotate
        self.img_unlock.theta = self.rotate
        if not self.scale:
            return
        if self.bar.horizontal:
            new_height = self.bar.height - (self.margin_y * 2)
            self.img_lock.resize(height=new_height)
            self.img_unlock.resize(height=new_height)
        else:
            new_width = self.bar.width - (self.margin_x * 2)
            self.img_lock.resize(width=new_width)
            self.img_unlock.resize(width=new_width)

    def draw(self):
        self.drawer.clear(self.bar.background)
        self.drawer.ctx.save()
        self.drawer.ctx.translate(self.margin_x, self.margin_y)
        if self.is_locked:
            self.drawer.ctx.set_source(self.img_lock.pattern)
        else:
            self.drawer.ctx.set_source(self.img_unlock.pattern)
        self.drawer.ctx.paint()
        self.drawer.ctx.restore()

        if self.bar.horizontal:
            self.drawer.draw(offsetx=self.offset, width=self.width)
        else:
            self.drawer.draw(offsety=self.offset, height=self.width)

    def calculate_length(self):
        if self.bar.horizontal:
            return self.img_lock.width + (self.margin_x * 2)
        else:
            return self.img_lock.height + (self.margin_y * 2)

    def change_lock(self, lock):
        if lock:
            self.is_locked = True
        else:
            self.is_locked = False
        self.draw()

    def cmd_lock(self):
        """Lock the keyboard"""
        self.change_lock(True)

    def cmd_unlock(self):
        """Unlock the keyboard"""
        self.change_lock(False)

    def cmd_toggle(self):
        """Toggle lock state"""
        self.change_lock(not self.is_locked)

    def button_press(self, x, y, button):
        if button == 1:
            self.change_lock(not self.is_locked)
