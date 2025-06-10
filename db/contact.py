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
        return results.to_dict(orient="records")

    def all(self):
        return self.data.to_dict(orient="records")

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

    def _get_id(self):
        return max(self.data["id"]) + 1

    def _flush_df_to_file(self):
        self.data.to_csv(self.csv_path, index=False)
