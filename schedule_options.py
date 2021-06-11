pln_to_byn_coeff = 0.68 # TODO: get this info from some API if possible

class ScheduleOption:
    def __init__(self, name, price_pln):
        self.name = name
        self.price = round(price_pln * pln_to_byn_coeff, 2)

    def notification_message(self):
        return f'Payday is here! Don\'t forget to pay {self.price} BYN for {self.name}.'


class ScheduleOptionManager:
    options = [ScheduleOption('netflix', 26), ScheduleOption('spotify', 5)]

    @classmethod
    def get_option(cls, option_name):
        return next((option for option in cls.options if option.name == option_name), None)
