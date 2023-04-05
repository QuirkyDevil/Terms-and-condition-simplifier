from __future__ import annotations
import asyncpg
from asyncpg.exceptions import PostgresError

from .drivers import Driver  # import the base driver impl


class PostgresDriver(Driver):
    """Asynchronous PostgreSQL driver implementation. This class inherits from the
    Driver class. This class contains the methods that are specific to
    PostgreSQL. This class also contains the connect method that will
    connect to the database and return the connection instance.
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
        """Add a row to the table and return whether the insert was done"""
        print("Adding to database")
        query = "INSERT INTO major_project (name, summary, last_updated) VALUES ($1, $2, $3)"
        try:
            async with self._connection.acquire() as conn:
                await conn.execute(query, company, summary, last_updated)
        except PostgresError:
            return False
        else:
            return True

    async def search(self, company: str):
        """Search for a row in the table and return the row"""
        query = "SELECT * FROM major_project WHERE name = $1"
        try:
            async with self._connection.acquire() as conn:
                row = await conn.fetchrow(query, company)
        except PostgresError:
            return None
        else:
            return row

    async def update(self, company: str, summary: str, last_updated: str):
        """Update a row in the table and return whether the update was done"""
        query = (
            "UPDATE major_project SET summary = $1, last_updated = $2 WHERE name = $3"
        )
        try:
            async with self._connection.acquire() as conn:
                await conn.execute(query, summary, last_updated, company)
        except PostgresError:
            return False
        else:
            return True

    async def delete(self, name: str) -> bool:
        """Delete a row from the table and return whether the delete was done"""
        try:
            async with self._connection.acquire() as conn:
                query = "DELETE FROM major_project " "WHERE name = $1"
                await conn.execute(query, name)
        except PostgresError:
            return False
        else:
            return True

    async def list_all(self):
        """Fetch all rows from the table and return them"""
        try:
            async with self._connection.acquire() as conn:
                query = "SELECT * FROM major_project"
                rows = await conn.fetch(query)
        except PostgresError:
            return []
        else:
            return rows

    async def cleanup(self) -> None:
        """called when shutting down the server to close the connection"""
        return await self._connection.close()


_DRIVER = PostgresDriver
_DRIVER_TYPE = "POSTGRES"
