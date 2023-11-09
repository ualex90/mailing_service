from random import shuffle


def get_random_list(model, quantity=3):
    """
    Получение списка случайных элементов
    model: Модель для выполнения запроса к базе данных
    quantity: максимальное количество элементов в списке (по умолчанию 3)
    """
    object_list = list(model.objects.all())
    shuffle(object_list)

    random_object_list = list()
    if len(object_list) >= quantity:
        for i in range(quantity):
            random_object_list.append(object_list.pop(0))
        return random_object_list
    return object_list
