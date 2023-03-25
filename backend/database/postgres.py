from __future__ import annotations
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
        self.table = table_name

        # Creating the table in psql on connect
        # if it doesn't exist.
        async with self._connection.acquire() as conn:
            query = f"CREATE TABLE IF NOT EXISTS {table_name} (name text PRIMARY KEY, summary text, last_updated timestamp);"

            await conn.execute(query)

        return self._connection

    async def add(self, company: str, summary: str, last_updated: str):
        """Add a row to the table"""
        print("Adding to database")
        query = f"INSERT INTO {self.table} (name, summary, last_updated) VALUES ($1, $2, $3)"
        try:
            async with self._connection.acquire() as conn:
                await conn.execute(query, company, summary, last_updated)
        except PostgresError:
            return False
        else:
            return True

    async def search(self, company: str):
        """Search for a row in the table"""
        query = f"SELECT * FROM {self.table} WHERE name = $1"
        try:
            async with self._connection.acquire() as conn:
                row = await conn.fetchrow(query, company)
        except PostgresError:
            return None
        else:
            return row

    async def update(self, company: str, summary: str, last_updated: str):
        """Update a row in the table"""
        query = (
            f"UPDATE {self.table} SET summary = $1, last_updated = $2 WHERE name = $3"
        )
        try:
            async with self._connection.acquire() as conn:
                await conn.execute(query, summary, last_updated, company)
        except PostgresError:
            return False
        else:
            return True

    async def delete(self, name: str) -> bool:
        """Delete a row from the table"""
        try:
            async with self._connection.acquire() as conn:
                query = f"DELETE FROM {self.table} " "WHERE name = $1"
                await conn.execute(query, name)
        except PostgresError:
            return False
        else:
            return True

    async def list_all(self):
        """Fetch all rows from the table"""
        try:
            async with self._connection.acquire() as conn:
                query = f"SELECT * FROM {self.table}"
                rows = await conn.fetch(query)
        except PostgresError:
            return []
        else:
            return rows

    async def cleanup(self) -> None:
        """called when shutting down the server"""
        return await self._connection.close()


_DRIVER = PostgresDriver
_DRIVER_TYPE = "POSTGRES"
