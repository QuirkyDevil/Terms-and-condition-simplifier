import zlib


class Driver:
    """The base driver class for all database drivers.
    Every database driver should inherit from this class. This class
    contains the basic methods that every database driver should have.
    The methods that are not implemented in the child class will raise
    a NotImplementedError. This class also contains a set_custom_val
    method that will help setting custom values that are not supported
    by the database driver. This method will also cache the values in
    the cache_values attribute. This attribute is a dictionary that
    contains the custom values that are set by the set_custom_val method.

    """

    def __init__(self):
        self._connection = None  # this connection instance
        # is filled in the connect method.
        self.identifier = None  # this is custom per database driver.
        # this attribute will be None until the connect method is called.
        self.cache_values = {}  # this will help setting custom values
        # with custom values that are set by the set_custom_val method.

    async def connect(self, **kwargs):
        """**[COMPULSARY]** Base driver connect method. This method should be implemented."""
        raise NotImplementedError

    async def add(self, *args, **kwargs):
        """**[COMPULSARY]** Base driver add method. This method should be implemented."""
        raise NotImplementedError

    async def search(self, *args, **kwargs):
        """**[COMPULSARY]** Base driver search method. This method should be implemented"""
        raise NotImplementedError

    async def update(self, *args, **kwargs):
        """**[COMPULSARY]** Base driver update method. This method should be implemented"""
        raise NotImplementedError

    async def delete(self, *args, **kwargs):
        """**[COMPULSARY]** Base driver delete method. This method should be implemented"""
        raise NotImplementedError

    async def list_all(self, *args, **kwargs):
        """**[COMPULSARY]** Base driver list_all method. This method should be implemented"""
        raise NotImplementedError

    async def cleanup(self):
        """**[COMPULSARY]** Base driver cleanup method. This method should be implemented"""
        raise NotImplementedError

    def set_custom_val(self, key: str, value: str):
        """set a custom value that is not supported by the database driver.
        This method will also cache the values in the cache_values attribute.
        This attribute is a dictionary that contains the custom values that
        are set by the set_custom_val method.
        """
        self.cache_values[key] = value
        return {key: value}

    @staticmethod
    def decompress(_bytes: bytes) -> bytes:
        """decompress the bytes, yet to be implemented"""
        decompressed = zlib.decompress(_bytes)
        return decompressed
