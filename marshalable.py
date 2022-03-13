import abc
import typing as T

class MarshalableRegistry(type):
    """Registry that stores all marshalables except base Marshalable class"""

    REGISTRY: T.Dict[str, "Marshalable"] = {}

    def __new__(cls, name, bases, attrs):
        new_cls = type.__new__(cls, name, bases, attrs)
        """
            Here the name of the class is used as key but it could be any class
            parameter.
        """
        if new_cls.object_type() is not None:
            cls.REGISTRY[new_cls.object_type()] = new_cls

        return new_cls

    @classmethod
    def get_registry(cls):
        return dict(cls.REGISTRY)

class ABCRegistryMeta(type(abc.ABC), MarshalableRegistry):
    pass

class Marshalable(metaclass=ABCRegistryMeta):
    @staticmethod
    @abc.abstractmethod
    def object_type() -> int:
        pass

    @abc.abstractmethod
    def get_fields(self) -> T.Dict[int, T.Any]:
        pass

    @staticmethod
    @abc.abstractmethod
    def from_fields(fields: T.Dict[int, T.Any]) -> "Marshalable":
        pass

if __name__ == "__main__":
    print(MarshalableRegistry.get_registry())
    class ExampleMarshalable(Marshalable):

        @staticmethod
        def object_type():
            return 1

        @staticmethod
        def from_fields(fields: T.Dict[int, T.Any]) -> "Marshalable":
            return ExampleMarshalable()

        def get_fields(self):
            return {}

    print(MarshalableRegistry.get_registry())
    print(ExampleMarshalable())
    print(ExampleMarshalable.from_fields({}))
