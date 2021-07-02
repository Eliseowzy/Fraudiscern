from abc import abstractmethod, ABCMeta


class model_interface:
    __metaclass__ = ABCMeta

    @abstractmethod
    def __str__(self):
        """Base interface: Convert the models into a human understandable string.
        """

    @abstractmethod
    def fit(self, train_set):
        """Base interface: Train the models

        Args:
            train_set (pyspark.sql.DataFrame): Train set.
        """
        pass

    @abstractmethod
    def validate_model(self, method):
        """Base interface: Validate models.

        Args:
            method (str): The validation method.
        """
        pass

    @abstractmethod
    def predict(self, test_set):
        """Base interface: Predict results on test_set.

        Args:
            test_set (pyspark.sql.DataFrame): Test set.
        """
        pass

    @abstractmethod
    def save_model(self, path):
        """
        Base interface: Save models
        Args:
            path (str): The target path.
        """
        pass

    @abstractmethod
    def load_model(self, path):
        """
        Base interface: Load an existing models from a file.
        Args:
            path (str): The source path.
        """
        pass

    @abstractmethod
    def optional_property(self):
        """Some optional features if necessary.
        """
        pass
