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

    async def add(self, name: str, summary: str, last_updated: str):
        """Add a row to the table"""
        query = {"_id": name, "summary": summary, "last_updated": last_updated}
        try:
            await self._connection.insert_one(query)
        except Exception:
            return False
        else:
            return True

    async def search(self, name: str) -> Mapping[str, Any] | None:
        """Search for a row in the table"""
        query = {"_id": name}
        try:
            values = await self._connection.find_one(query)
        except Exception:
            return None
        else:
            return values

    async def update(self, name: str, summary: str, last_updated: str) -> bool:
        """Update a row in the table"""
        query = {"_id": name}
        new_values = {"$set": {"summary": summary, "last_updated": last_updated}}
        try:
            await self._connection.update_one(query, new_values)
        except Exception:
            return False
        else:
            return True

    async def delete(self, name: str) -> bool:
        # Returns whether the delete succeeded or failed
        query = {"_id": name}
        try:
            await self._connection.delete_one(query)
        except Exception:
            return False
        else:
            return True

    async def list_all(self) -> Tuple[List[Mapping[str, Any]], str]:
        documents = await self._connection.find({}).to_list(
            length=99999999999999999999
        )  # big number
        return (documents, "_id")

    async def cleanup(self):
        return self._parent_client.close()


_DRIVER = MongoDriver
_DRIVER_TYPE = "MONGO"
