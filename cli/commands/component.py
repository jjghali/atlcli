import click
import pprint36 as pprint

from pretty_tables import PrettyTables
from services import BitbucketService


bitbucketInstance = BitbucketService()
jiraInstance = {}


@click.group()
@click.pass_context
def component(ctx):
    """Get information about a component"""
    # context_parent = click.get_current_context()
    # ctx.ensure_object(dict)
    # ctx.obj['COMPONENT_NAME'] = component_name
    pass


@component.group(chain=False, invoke_without_command=True)
@click.pass_context
@click.option('-c', '--component-name', default=False)
@click.option('-v', '--version', default="")
@click.option('--include-unstable/--only-stable', required=False, default=False)
def release(ctx, component_name, version, include_unstable):
    changelog = bitbucketInstance.getRelease(component_name, version)
    print(changelog)


@release.command()
@click.pass_context
def tasks(ctx):
    headers = ["TASK", "Description", "Status"]
    rows = [
        ["DD-1234", "Description de la tache", "En cours"],
        ["DD-1235", "Description de la tache", "En cours"],
        ["DD-1236", "Description de la tache", "En cours"],
    ]

    table = PrettyTables.generate_table(
        headers=headers,
        rows=rows,
        empty_cell_placeholder="No Data"
    )
    print("Tasks for {product}/{component} {version}\n".format(
        product=ctx.obj["PRODUCT_NAME"],
        component=ctx.obj["COMPONENT_NAME"],
        version=ctx.obj["VERSION"]
    ))

    print(table)