from __future__ import annotations

from typing import Any, Tuple, Mapping, List

from motor.motor_asyncio import AsyncIOMotorCollection, AsyncIOMotorClient
from .drivers import Driver  # import the base driver impl


class MongoDriver(Driver):
    """
    Custom implementation of the Driver class for mongoDB,
    as we just need to add methods to this file and not modify the entire codebase.
    """

    async def connect(self, **kwargs):
        self.identifier = "mongo"

        connection_uri = kwargs["connection_uri"]
        database_name = kwargs["database_name"]
        collection_name = kwargs["collection_name"]

        client = AsyncIOMotorClient(connection_uri)
        _db = client[database_name]
        coll = _db[collection_name]
        self._connection: AsyncIOMotorCollection = coll

        # custom attributes
        self._parent_client = client
        return self._connection

    async def insert(self):
        return

    async def fetch(self):
        return

    async def delete(self, name: str) -> bool:
        # Returns whether the delete succeeded or failed
        query = {"_id": name}
        try:
            await self._connection.delete_one(query)
        except Exception:
            return False
        else:
            return True

    async def fetch_all(self) -> Tuple[List[Mapping[str, Any]], str]:
        documents = await self._connection.find({}).to_list(
            length=99999999999999999999
        )  # big number
        return (documents, "_id")

    async def cleanup(self):
        return self._parent_client.close()


_DRIVER = MongoDriver
_DRIVER_TYPE = "MONGO"
