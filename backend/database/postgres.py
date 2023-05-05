from _future_ import annotations
import asyncpg
import asyncio
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
            query = f"CREATE TABLE IF NOT EXISTS {table_name} (name text PRIMARY KEY, summary text, last_updated timestamp, link text);"

            await conn.execute(query)

        return self._connection

    async def add(self, company: str, summary: str, last_updated: str, link: str):
        """Add a row to the table and return whether the insert was done"""
        query = "INSERT INTO major_project (name, summary, last_updated, link) VALUES ($1, $2, $3, $4)"
        try:
            async with self._connection.acquire() as conn:
                await conn.execute(query, company, summary, last_updated, link)
        except PostgresError as e:
            print(e)
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

    async def update(self, company: str, summary: str, last_updated: str, link: str):
        """Update a row in the table and return whether the update was done"""
        query = "UPDATE major_project SET summary = $1, last_updated = $2, link = $3 WHERE name = $4"
        try:
            async with self._connection.acquire() as conn:
                await conn.execute(query, summary, last_updated, link, company)
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

    async def count(self):
        """Count the number of rows in the table and return the count"""
        try:
            async with self._connection.acquire() as conn:
                query = "SELECT COUNT(*) FROM major_project"
                count = await conn.fetchval(query)
        except PostgresError:
            return 0
        else:
            return count

    async def fill_cache(self):
        """Fill the cache with the rows from the table"""
        try:
            async with self._connection.acquire() as conn:
                query = "SELECT * FROM major_project"
                rows = await conn.fetch(query)
        except PostgresError:
            return False
        else:
            # to dict where key is name and value is the row except name
            data = {row[0]: row[1:] for row in rows}
            return data

    async def purge(self):
        """Purge the table"""
        try:
            async with self._connection.acquire() as conn:
                query = "DELETE FROM major_project"
                await conn.execute(query)
        except PostgresError:
            return False
        else:
            return True

    async def drop_table(self):
        """Drop the table"""
        try:
            async with self._connection.acquire() as conn:
                query = "DROP TABLE major_project"
                await conn.execute(query)
        except PostgresError:
            return False
        else:
            return True

    async def cleanup(self) -> None:
        """called when shutting down the server to close the connection"""
        return await self._connection.close()


_DRIVER = PostgresDriver
_DRIVER_TYPE = "POSTGRES"


if _name_ == "_main_":

    async def main():
        driver = _DRIVER()
        try:
            await driver.connect(
                connection_uri="",
                max_size=100,
                min_size=75,
                table_name="",
            )
        except:
            print("Error")
        else:
            print("Success")

    asyncio.run(main())
