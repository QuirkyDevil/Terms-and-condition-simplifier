from __future__ import annotations

from typing import Mapping, List, Any

import asyncpg
from asyncpg.exceptions import PostgresError

from .drivers import Driver  # import the base driver impl


class PostgresDriver(Driver):
    """
    Custom implementation of the Driver class for postgres,
    as we just need to add methods to this file and not modify the entire codebase.
    """

    async def connect(self, **kwargs):
        """Connect to a psql database using the kwargs provided in config.py"""
        self.identifier = "postgres"

        connection_uri = kwargs["connection_uri"]
        max_size = kwargs["max_size"]
        min_size = kwargs["min_size"]
        table_name = kwargs["table_name"]

        pool = await asyncpg.create_pool(
            connection_uri, min_size=min_size, max_size=max_size
        )

        self._connection = pool

        # Creating the table in psql on connect
        # if it doesn't exist.
        async with self._connection.acquire() as conn:
            query = f"CREATE TABLE IF NOT EXISTS {table_name}()"

            await conn.execute(query)

        return self._connection

    async def insert(self):
        """Need to implement this for different tables which are yet to be decided"""
        return

    async def fetch(self):
        """Need to implement this for different tables which are yet to be decided"""
        return

    async def delete_row(self, name: str) -> bool:
        """Delete a row from the table"""
        table_name = "test"
        try:
            async with self._connection.acquire() as conn:
                query = f"DELETE FROM {table_name} " "WHERE name = $1"
                await conn.execute(query, name)
        except PostgresError:
            return False
        else:
            return True

    async def fetch_all(self, table_name: str) -> List[Mapping[str, Any]]:
        """Fetch all rows from the table"""
        async with self._connection.acquire() as conn:
            rows = await conn.fetch(f"SELECT * FROM {table_name}")
        return (rows, "name")

    async def cleanup(self):
        """called when shutting down the server"""
        return await self._connection.close()


_DRIVER = PostgresDriver
_DRIVER_TYPE = "POSTGRES"
