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
    name = State()
    order = State()
    check = State()


class Send_post_code(StatesGroup):
    id = State()
    wait_for_post_code = State()