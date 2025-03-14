class MoveException(Exception):
    def __init__(self, error_message):
        self._error_msg = error_message

    def __str__(self):
        return str(self._error_msg)


class PositionAlreadyTaken(MoveException):
    def __init__(self):
        MoveException.__init__(self, "The position is already taken")


class NotAValidPosition(MoveException):
    def __init__(self):
        MoveException.__init__(self, "Not a valid position (must be 01, 02, ...24")


class NotOwner(MoveException):
    def __init__(self):
        MoveException.__init__(self, "Not your position")


class NotFreePosition(MoveException):
    def __init__(self):
        MoveException.__init__(self, "Not free position")


class NotAdiacentPosition(MoveException):
    def __init__(self):
        MoveException.__init__(self, "Not adiacent position (stage 2)")


class NotEnemy(MoveException):
    def __init__(self):
        MoveException.__init__(self, "This position doesn't belong to the computer. Pick a valid one to remove.")


class MillTakingPlace(MoveException):
    def __init__(self):
        MoveException.__init__(self, "This position belongs to a mill and can't be taken.")
