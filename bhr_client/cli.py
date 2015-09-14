import click
import getpass
from bhr_client.rest import login, login_from_env

@click.group()
@click.option("--host",     envvar="BHR_HOST",      default="http://localhost")
@click.option("--username", "-u", envvar="BHR_USERNAME",  default=None)
@click.option("--password", "-p", envvar="BHR_PASSWORD",  default=None)
@click.option("--token",    "-t", envvar="BHR_TOKEN",     default=None)
@click.option("--ssl-no-verify", "-S", envvar="BHR_SSL_NO_VERIFY", default=False, is_flag=True)
@click.pass_context
def cli(ctx, host, username, password, token, ssl_no_verify):
    if username and not password:
        password = getpass.getpass("Password: ")
    client = login(host, token=token, username=username, password=password, ssl_no_verify=ssl_no_verify)
    ctx.obj = client

@cli.command()
@click.argument('cidr')
@click.pass_obj
def query(client, cidr):
    for r in client.query(cidr):
        click.echo("{cidr} {added} {unblock_at} {source} {who} {why}".format(**r))

@cli.command()
@click.pass_obj
def list(client):
    for r in client.get_expected():
        click.echo(r['cidr'])

@cli.command()
@click.pass_obj
def stats(client):
    stats = client.stats()
    for k, v in stats.items():
        K = k.replace("_", " ").title()
        K = click.style(k, fg="green")
        click.echo("%s: %d" % (K, v))

@cli.command()
@click.argument('cidr', nargs=-1)
@click.option('--source', '-s', default='cli')
@click.option('--why', '-w', required=True)
@click.option('--duration', '-d', default='1d')
@click.option('--autoscale', '-a', is_flag=True, default=False)
@click.option('--skip-whitelist', is_flag=True, default=False)
@click.pass_obj
def block(client, cidr, source, why, duration, autoscale, skip_whitelist):
    for addr in cidr:
        block = client.block(cidr=addr, source=source, why=why, duration=duration, autoscale=autoscale, skip_whitelist=skip_whitelist)
        if 'cidr' in block:
            click.echo("{cidr} {source} {who} {why} {added} {unblock_at}".format(**block))
        else:
            click.secho(str(block), fg='red')

@cli.command()
@click.argument('cidr', nargs=-1)
@click.option('--why', '-w', required=True)
@click.pass_obj
def unblock(client, cidr, why):
    for addr in cidr:
        resp = client.unblock_now(cidr=addr, why=why)
        click.echo(resp)

def main():
    cli()
