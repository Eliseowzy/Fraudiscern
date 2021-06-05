from abc import abstractmethod, ABCMeta


class ModelInterface:
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self):
        """
        Base Interface: Initialize the model by setting model name and model object.
        """
        raise NotImplementedError("You must implement ModelInterface.__init__() interface!")

    @abstractmethod
    def __str__(self):
        """
        Base Interface: Convert the model into a human understandable string.
        :return: An string object.
        """
        raise NotImplementedError("You must implement ModelInterface.__str__() interface!")

    @abstractmethod
    def load_data(self):
        """
        Base Interface: Load the dataset.
        :return: None
        """
        raise NotImplementedError("You must implement ModelInterface.load_data() interface!")

    @abstractmethod
    def set_model_parameters(self, parameters):
        """
        Base Interface: Set model parameters.
        :param parameters:
        :return:
        """
        raise NotImplementedError("You must implement ModelInterface.set_model_parameters() interface!")

    @abstractmethod
    def get_model_parameters(self):
        """
        Base Interface: Get the parameters of the model.
        :return:
        """
        raise NotImplementedError("You must implement ModelInterface.get_model_parameters() interface!")

    @abstractmethod
    def fit(self, train_set):
        """
        Base Interface: Train the model
        :param train_set:
        :return:
        """
        raise NotImplementedError("You must implement ModelInterface.train() interface!")

    @abstractmethod
    def validate_model(self):
        """
        Base Interface: Validate model.
        :return:
        """
        print("ModelInterface.validate() is an optional property.")

    @abstractmethod
    def predict(self, test_set):
        """
        Base Interface: Predict results on test_set.
        :param test_set:
        :return:
        """
        raise NotImplementedError("You must implement ModelInterface.predict() interface!")

    @abstractmethod
    def save_model(self):
        """
        Base Interface: Save model
        :return:
        """
        print("ModelInterface.save_model() is an optional property.")
        pass

    @abstractmethod
    def load_model(self, path):
        """
        Base interface: Load an existing model from a file.
        :param path:
        :return:
        """
        raise NotImplementedError("You must implement ModelInterface.set_model_name() interface!")

    @abstractmethod
    def optional_property(self):
        print("ModelInterface.property() is an optional property")
