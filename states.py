from aiogram.fsm.state import StatesGroup, State



class Add_new_prod(StatesGroup):
    name = State()
    about = State()
    price = State()
    photo = State()
    verif = State()

class Delete_prod(StatesGroup):
    name_of_it = State()
    rep = State()



class Buy_item(StatesGroup):
    address = State()
    phone_number = State()
    order = State()
    check = State()
