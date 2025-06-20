class Contact:
    def __init__(
        self,
        id=None,
        first_name=None,
        last_name=None,
        phone=None,
        email=None,
        errors=None,
    ):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.email = email
        self.errors = errors if errors else {}
