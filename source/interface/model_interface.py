from abc import abstractmethod, ABCMeta


class model_interface:
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self):
        """
        Base interface: Initialize the models by setting models name and models object.
        """
        raise NotImplementedError("You must implement ModelInterface.__init__() interface!")

    @abstractmethod
    def __str__(self):
        """
        Base interface: Convert the models into a human understandable string.
        :return: An string object.
        """
        raise NotImplementedError("You must implement ModelInterface.__str__() interface!")

    @abstractmethod
    def fit(self, train_set):
        """
        Base interface: Train the models
        :param train_set:
        :return:
        """
        raise NotImplementedError("You must implement ModelInterface.train() interface!")

    @abstractmethod
    def validate_model(self, method):
        """
        Base interface: Validate models.
        :return:
        """
        print("ModelInterface.validate() is an optional property.")

    @abstractmethod
    def predict(self, test_set):
        """
        Base interface: Predict results on test_set.
        :param test_set:
        :return:
        """
        raise NotImplementedError("You must implement ModelInterface.predict() interface!")

    @abstractmethod
    def save_model(self, path):
        """
        Base interface: Save models
        :return:
        """
        print("ModelInterface.save_model() is an optional property.")
        pass

    @abstractmethod
    def load_model(self, path):
        """
        Base interface: Load an existing models from a file.
        :param path:
        :return:
        """
        raise NotImplementedError("You must implement ModelInterface.set_model_name() interface!")

    @abstractmethod
    def optional_property(self):
        print("ModelInterface.property() is an optional property")
