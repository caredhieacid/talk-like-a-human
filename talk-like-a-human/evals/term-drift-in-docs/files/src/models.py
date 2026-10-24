class Workspace:
    """A workspace groups projects and members. Billing is per workspace."""

    def __init__(self, name: str, seats: int = 10):
        self.name = name
        self.seats = seats
        self.members: list["Member"] = []


class Member:
    def __init__(self, user_id: str, workspace: Workspace):
        self.user_id = user_id
        self.workspace = workspace
