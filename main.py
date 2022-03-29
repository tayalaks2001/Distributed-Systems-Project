import click

from server import AtleastOnceServer, AtmostOnceServer


@click.command()
@click.option('--atleast-once/--atmost-once', default=True, show_default=True)
@click.option('--success-prob', default=1.0, show_default=True)
@click.option('--port', default=2222, show_default=True)
def start_server(atleast_once, success_prob, port):
    """Simple program that greets NAME for a total of COUNT times."""
    if atleast_once:
        print(f"Starting Atleast once server on port {port}")
        s = AtleastOnceServer("0.0.0.0", port, success_prob=success_prob)
    else:
        print(f"Starting Atmost once server on port {port}")
        s = AtmostOnceServer("0.0.0.0", port, success_prob=success_prob)
        
    s.server_loop()

if __name__ == '__main__':
    start_server()
