from datetime import datetime


class Package(object):
    def __init__(self, data):
        self.id = data.get("key")
        self.name = data.get("title")
        self.type = data.get("settings").get("box")
        self.status = data.get("status").get("deliveryStatus")
        self.status_message = data.get("status").get("phase").get("message")
        self.delivery_date = None
        if data.get("status").get("delivery").get("deliveryDate") is not None:
            self.delivery_date = datetime.fromisoformat(
                data.get("status").get("delivery").get("deliveryDate")
            )
        self.planned_date = None
        self.planned_from = None
        self.planned_to = None
        if (
            data.get("status").get("enroute") is not None
            and data.get("status").get("enroute").get("timeframe") is not None
            and data.get("status").get("enroute").get("timeframe").get("date") is not None
        ):
            self.planned_date = datetime.fromisoformat(
                data.get("status").get("enroute").get("timeframe").get("date")
            )
            self.planned_from = (
                data.get("status").get("enroute").get("timeframe").get("from")
            )
            self.planned_to = (
                data.get("status").get("enroute").get("timeframe").get("to")
            )
        self.url = data.get("status").get("webUrl")

    @property
    def is_delivered(self):
        return self.status == "Delivered"

    @property
    def delivery_today(self):
        return self.delivery_date.date() == datetime.today().date()

    def __str__(self):
        return f"{self.id} {self.name} {self.type} {self.status} {self.status_message} {self.delivery_date.date() if self.delivery_date else 'Unknown'} {self.planned_date} {self.planned_from} {self.planned_to}"
