from random import uniform, seed
from configuration import logger


class LayerBuilder:
    """
    Класс для построения слоёв нейронной сети.
    Содержит методики для генерации весов, вычисления данных нейронов и различных активационных функций.
    """
    _test_mode = False

    def __repr__(self):
        """
        Возвращает строковое представление объекта LayerBuilder.
        :return: Строковое представление объекта.
        """
        return f'Модуль: {__name__}; Класс: {self.__class__.__name__}; Адрес в памяти: {hex(id(self))}\n'

    @classmethod
    def _initialize_weights(cls, input_size: int, neuron_number: int) -> list[list[float]]:
        """
        Генерирует размеры весов для нейронов.
        :param input_size: Размер списка входных данных.
        :param neuron_number: Количество нейронов.
        :return: Массив из списков весов.
        """
        if cls._test_mode:
            seed(0)  # Фиксация предсказуемых значений для тестирования
        logger.info(f'Генерация весов для входных данных размером {input_size} и {neuron_number} нейронов.')
        return [[uniform(-0.01, 0.01) for _ in range(input_size)] for _ in range(neuron_number)]

    @staticmethod
    def _verify_switch_type(switch: bool | list[bool], neuron_number: int) -> list[bool]:
        """
        Проверяет тип переключателя для нейронов.
        :param switch: Булевое значение или список булевых значений.
        :param neuron_number: Количество нейронов.
        :return: Список булевых значений.
        """
        if isinstance(switch, bool):
            logger.info(f'Преобразование булевого значения {switch} в список из {neuron_number} элементов.')
            return [switch] * neuron_number
        elif isinstance(switch, list):
            logger.info(f'Использование переданного списка булевых значений {switch}.')
            return switch
        raise ValueError(f'Значение "{switch}" должно быть {bool} или {list}!')

    @classmethod
    def _calculate_neuron_dataset(
            cls, input_dataset: list[int | float], neuron_number: int,
            weights: list[list[int | float]], bias: float, switch: bool | list[bool]
    ) -> list[float]:
        """
        Вычисляет значения массива данных нейронов с заданными параметрами.
        :param input_dataset: Список входных данных.
        :param neuron_number: Количество нейронов.
        :param weights: Список весов нейронов.
        :param bias: Смещение.
        :param switch: Булевое значение или список булевых значений.
        :return: Список результатов обработки данных нейронов.
        """
        if cls._test_mode:
            seed(0)  # Фиксация предсказуемых значений для тестирования
        logger.info(f'Вычисление данных для {neuron_number} нейронов с bias={bias}.')
        neuron_dataset = []
        switch_list = cls._verify_switch_type(switch, neuron_number)
        for n in range(neuron_number):
            neuron_dataset.append(
                [i * w + bias if switch_list[n] else i * w - bias for i, w in zip(input_dataset, weights[n])]
            )
        result = [sum(i) for i in neuron_dataset]
        logger.info(f'Результаты вычислений: {result}')
        return result


class ActivationFunctions:
    @staticmethod
    def get_linear(x):
        """
        Линейная активационная функция.
        :param x: Входное значение.
        :return: То же входное значение.
        """
        return x

    @staticmethod
    def get_relu(x):
        """
        ReLU (Rectified Linear Unit) активационная функция.
        :param x: Входное значение.
        :return: Максимум между нулем и входным значением.
        """
        return max(0, x)

    @staticmethod
    def get_sigmoid(x):
        """
        Сигмоидная активационная функция.
        :param x: Входное значение.
        :return: Значение сигмоидной функции для входного значения.
        """
        n = 10
        exp = 1.0
        for i in range(n, 0, -1):
            exp = 1 + x * exp / i
        return 1 / (1 + exp)

    @staticmethod
    def get_tanh(x):
        """
        Активационная функция гиперболический тангенс (tanh).
        :param x: Входное значение.
        :return: Значение функции tanh для входного значения.
        """
        e_pos_2x = 1.0
        e_neg_2x = 1.0
        n = 10
        for i in range(n, 0, -1):
            e_pos_2x = 1 + 2 * x * e_pos_2x / i
            e_neg_2x = 1 - 2 * x * e_neg_2x / i
        return (e_pos_2x - e_neg_2x) / (e_pos_2x + e_neg_2x)

    @staticmethod
    def get_solution(x, bias):
        if x > 0:
            return x + bias
        return x - bias


class InputLayer(LayerBuilder):
    """
    Класс для входного слоя нейронной сети, наследуется от LayerBuilder.
    Выполняет начальную обработку входных данных, применяя указанную активационную функцию.
    """

    def __init__(self, input_dataset: list[int | float], activation_function_first, activation_function_second):
        """
        Инициализирует входной слой.
        :param input_dataset: Список входных данных.
        :param activation_function_first: Функция активации первого нейрона.
        :param activation_function_second: Функция активации второго нейрона.
        """
        if self._test_mode:
            seed(0)
        self.input_dataset = input_dataset
        self.input_size = len(input_dataset)
        self.__neuron_number = 2
        self.weights = self._initialize_weights(self.input_size, self.__neuron_number)
        self.bias = uniform(-0.01, 0.01)
        self.switch_list = [True, True]
        self.activation_function_first = activation_function_first
        self.activation_function_second = activation_function_second

    def _reset__init__(self):
        return self.__init__(self.input_dataset, self.activation_function_first, self.activation_function_second)

    def get_layer_dataset(self) -> list[float]:
        """
        Получает массив данных слоя с примененной активационной функцией.
        :return: Список значений после применения активационной функции.
        """
        neuron_data_first, neuron_data_second = self._calculate_neuron_dataset(
            self.input_dataset, self.__neuron_number, self.weights, self.bias, self.switch_list
        )
        logger.debug(self)
        return [self.activation_function_first(neuron_data_first), self.activation_function_second(neuron_data_second)]


class DeepLayer(LayerBuilder):
    """
    Класс для глубокого слоя нейронной сети, наследуется от LayerBuilder.
    Обрабатывает данные слоями, создавая сложные представления входных данных.
    """

    def __init__(self, input_dataset: list[int | float], neuron_number: int, activation_function):
        """
        Инициализирует глубокий слой.
        :param input_dataset: Список входных данных.
        :param neuron_number: Количество нейронов.
        :param activation_function: Функция активации для слоя.
        """
        if self._test_mode:
            seed(0)
        self.input_dataset = input_dataset
        self.input_size = len(input_dataset)
        self.neuron_number = neuron_number
        self.weights = self._initialize_weights(self.input_size, neuron_number)
        self.bias = uniform(-0.01, 0.01)
        self.activation_function = activation_function

    def _reset__init__(self):
        return self.__init__(self.input_dataset, self.neuron_number, self.activation_function)

    def get_layer_dataset(self) -> list[float]:
        """
        Получает массив данных слоя с примененной активационной функцией.
        :return: Список значений после применения активационной функции.
        """
        result = self._calculate_neuron_dataset(self.input_dataset, self.neuron_number, self.weights, self.bias, True)
        logger.debug(self)
        return [self.activation_function(i) for i in result]


class OutputLayer(LayerBuilder):
    """
    Класс для выходного слоя нейронной сети, наследуется от LayerBuilder.
    Завершает обработку данных и возвращает конечный результат.
    """

    def __init__(self, input_dataset, activation_function):
        """
        Инициализирует выходной слой.
        :param input_dataset: Список входных данных.
        :param activation_function: Функция активации для слоя.
        """
        if self._test_mode:
            seed(0)  # Фиксация предсказуемых значений для тестирования
        self.input_dataset = input_dataset
        self.bias = uniform(-0.01, 0.01)
        self.activation_function = activation_function

    def get_layer_dataset(self) -> int | float:
        """
        Получает массив данных слоя с примененной активационной функцией.
        :return: Значение после применения активационной функции.
        """
        result = sum(self.input_dataset)
        return self.activation_function(result)


class NeuralNetwork(ActivationFunctions, LayerBuilder):
    """
    Класс для построения и управления нейронной сетью, наследуется от LayerBuilder.
    Управляет различными слоями и их взаимодействием.
    """

    def __init__(self, input_dataset):
        """
        Инициализирует нейронную сеть.
        :param input_dataset: Список входных данных.
        """
        self.input_dataset = self.validate_input_dataset(input_dataset)
        self.layers = {}

    @staticmethod
    def validate_input_dataset(input_dataset):
        """
        Проверяет корректность входных данных.
        :param input_dataset: Список входных данных.
        :return: Проверенный список входных данных.
        :raises ValueError: Если входные данные некорректны.
        """
        if not isinstance(input_dataset, list):
            raise ValueError(f'Значение "{input_dataset}" должно быть списком!')
        if not all(isinstance(x, (int, float)) for x in input_dataset):
            raise ValueError(f'Все элементы списка "{input_dataset}" должны быть целыми или вещественными числами!')
        return input_dataset

    @staticmethod
    def propagate(layer):
        """
        Пропускает данные через слой.
        :param layer: Объект слоя.
        :return: Данные слоя.
        """
        return layer.get_layer_dataset()

    def add_layer(self, name: str, layer):
        """
        Добавляет слой в нейронную сеть.
        :param name: Название слоя.
        :param layer: Объект слоя.
        """
        logger.info(f'Добавление слоя "{name}" в сеть.')
        self.layers[name] = layer

    def remove_layer(self, name: str):
        """
        Удаляет слой из нейронной сети.
        :param name: Название слоя.
        """
        if name in self.layers:
            logger.info(f'Удаление слоя "{name}" из сети.')
            del self.layers[name]
        else:
            logger.warning(f'Слой "{name}" не найден при попытке удаления.')

    def get_layer(self, name: str):
        """
        Возвращает слой по его имени.
        :param name: Название слоя.
        :return: Объект слоя или None, если слой не найден.
        """
        return self.layers.get(name)

    def build_neural_network(self):
        """
        Строит нейронную сеть, добавляя входной, глубокие и выходной слои.
        """
        logger.info('Начало построения нейронной сети.')
        input_layer = InputLayer(self.input_dataset, self.get_linear, self.get_linear)
        self.add_layer('input_layer', input_layer)
        logger.debug(f'Входной слой создан с параметрами: {input_layer}')

        deep_layer_first = DeepLayer(self.propagate(input_layer), 3, self.get_tanh)
        self.add_layer('deep_layer_first', deep_layer_first)
        logger.debug(f'Первый глубокий слой создан с параметрами: {deep_layer_first}')

        deep_layer_second = DeepLayer(self.propagate(deep_layer_first), 2, self.get_tanh)
        self.add_layer('deep_layer_second', deep_layer_second)
        logger.debug(f'Второй глубокий слой создан с параметрами: {deep_layer_second}')

        output_layer = OutputLayer(self.propagate(deep_layer_second), self.get_sigmoid)
        self.add_layer('output_layer', output_layer)
        logger.debug(f'Выходной слой создан с параметрами: {output_layer}')

        logger.info('Построение нейронной сети завершено.')

    def get_visualisation(self):
        """
        Выводит визуальное представление нейронной сети.
        """
        print(f'Класс: {self.__class__.__name__}')
        print(f'Всего слоёв: {len(self.layers)}')
        print(f'Входные данные: {self.input_dataset}\n')
        for name, layer in self.layers.items():
            print(f'Слой: {name}')
            print(f'Данные слоя: {layer.get_layer_dataset()}\n')
