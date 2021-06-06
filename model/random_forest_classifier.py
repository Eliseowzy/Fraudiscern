from sklearn.ensemble import RandomForestClassifier

from utils import data_loader
from interface.model_interface import model_interface


class RandomForestClassifierModel(model_interface):
    """
    This is an example for implementing the model interface
    """

    def __init__(self):
        # self._model_name = model_name
        # super().__init__(model_object)
        self._model_object = None
        self._predict_result = None

    def __str__(self):
        return str(self._model_object)

    def setup_data(self, path=None):
        data_loader.load_data_from_csv("sample_data.csv")
        dataset = data_loader.get_dataset()
        # self.load_some_data()
        # Implement load data function here.
        return None

    def load_model(self, path):
        # self._model = self._model.load_my_model(path)
        return None

    def set_model_parameters(self, parameters):
        self._model = "new model with new parameters: {}".format(parameters)
        return None

    def get_model_parameters(self):
        parameters = "A function to get parameters of the _model"
        return parameters

    def fit(self, train_set):
        print("The model is training")
        print("self._model.fit()")
        # self._model = self._model.fit()
        return None

    def predict(self, test_set):
        # test_set_X, test_set_y = a_function_split(test_set)
        # self._predict_result = self._model.my_model_predict(test_set_X)
        # auc_validation(self._predict_result, test_set_y)
        print("The model is used to predict")

    def save_model(self):
        print("Implement your model save function here!")
        # self._model.save()

    def validate_model(self):
        print("Implement model validation here.")
        # Some model validation code here

    def optional_property(self):
        print("You can write some other unique functions here")
