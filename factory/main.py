import time

import click
from bulk import BulkFactory
from database import delete_data, init_db


@click.command()
@click.option("--host", default="", envvar="DB_HOST", help="The hostname of the target database")
@click.option("--user", default="", envvar="DB_USER", help="The database user to connect as")
@click.option(
    "--password", default="", envvar="DB_PASSWORD", help="The password for the database user"
)
@click.option("--database", default="", envvar="DB_NAME", help="The database to use by default")
@click.option("--album-count", default=10000, help="The number of albums to create")
@click.option("--batch-size", default=5000, help="The batch size for write operations")
@click.option("--schema-only", is_flag=True, help="Only apply the database schema")
@click.option("--flush", is_flag=True, help="Delete all existing data")
def cmd(host, user, password, database, album_count, batch_size, schema_only, flush):
    """Create a set of fake albums on the target database"""
    start = time.time()
    if any((not val for val in (host, user, password, database))):
        click.echo("Missing db connection info, using in memory sqlite db")
        db_type = "sqlite"
    else:
        db_type = "mysql"
    Session = init_db(db_type, user, password, host, database)

    if schema_only:
        click.echo(f"Done in {time.time() - start}s")
        return

    if flush:
        click.echo("Deleting current data...")
        delete_data()

    click.echo(f"Creating {album_count} albums and associated data...")
    factory = BulkFactory(Session)
    factory(album_count, batch_size)

    click.echo(f"Done in {time.time() - start}s")


if __name__ == "__main__":
    cmd()
