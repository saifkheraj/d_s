import click
from mylib.bot import scrape


@click.command()
@click.option("--name", prompt="wikipedia page", help="your wikipedia page")
def cli(name, length=1):
    result = scrape(name, 1)
    click.echo({result})
    return result


if __name__ == "__main__":
    cli()
