from shiftregister import ShiftRegister

register = ShiftRegister(9, 10, 11)
register.show()  # Clear to zero
register.shift(1)
register.shift(0)
register.show()
