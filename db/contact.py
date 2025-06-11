import pandas as pd
from model.contact import Contact


class ContactDB:
    def __init__(self, csv_path):
        self.csv_path = csv_path
        self.data = pd.read_csv(csv_path)

    def search(self, query: str):
        query = query.lower()
        results = self.data[
            (self.data["first_name"] == query) | (self.data["last_name"] == query)
        ]
        results_dicts = results.to_dict(orient="records")
        return [
            Contact(
                contact_dict["id"],
                contact_dict["first_name"],
                contact_dict["last_name"],
                contact_dict["phone"],
                contact_dict["email"],
            )
            for contact_dict in results_dicts
        ]

    def find(self, id: int):
        result = self.data[self.data["id"] == id]
        contact_dict = result.to_dict(orient="records")[0]
        contact = Contact(
            contact_dict["id"],
            contact_dict["first_name"],
            contact_dict["last_name"],
            contact_dict["phone"],
            contact_dict["email"],
        )
        return contact

    def all(self):
        all_contacts = self.data.to_dict(orient="records")
        return [
            Contact(
                contact_dict["id"],
                contact_dict["first_name"],
                contact_dict["last_name"],
                contact_dict["phone"],
                contact_dict["email"],
            )
            for contact_dict in all_contacts
        ]

    def create(self, contact: Contact):
        id = self._get_id()
        row = {
            "id": id,
            "first_name": contact.first_name,
            "last_name": contact.last_name,
            "phone": contact.phone,
            "email": contact.email,
        }
        new_row_df = pd.DataFrame([row])
        self.data = pd.concat([self.data, new_row_df], ignore_index=True)
        self._flush_df_to_file()
        return True

    def update(self, contact: Contact):
        def update_closure(row):
            if row["id"] == contact.id:
                row["first_name"] = contact.first_name
                row["last_name"] = contact.last_name
                row["phone"] = contact.phone
                row["email"] = contact.email
            return row

        self.data = self.data.apply(update_closure, axis=1)
        self._flush_df_to_file()
        return True

    def delete(self, id: int):
        self.data = self.data[self.data["id"] != id]
        self._flush_df_to_file()

    def _get_id(self):
        return max(self.data["id"]) + 1

    def _flush_df_to_file(self):
        self.data.to_csv(self.csv_path, index=False)
