import click
from core.code_ingestor import CodeIngestor
from core.vector_indexer import VectorIndexer
from core.llm_interface import QwenCodeAnalyzer
from cli.formatters import format_response


@click.group()
def cli():
    pass


@cli.command()
@click.argument('source')
def ingest(source):
    ingestor = CodeIngestor()
    indexer = VectorIndexer()

    if source.startswith('http'):
        chunks = ingestor.load_from_git(source)
    else:
        chunks = ingestor.load_from_source(source)

    indexer.index_code(chunks, [{} for _ in chunks])
    click.echo(f"Indexed {len(chunks)} code chunks")


@cli.command()
@click.option('--query', prompt='Your code question')
def ask(query):
    indexer = VectorIndexer()
    analyzer = QwenCodeAnalyzer()

    context = indexer.search(query)
    response = analyzer.generate_response(query, "\n".join(context))
    format_response(query, [response])


if __name__ == '__main__':
    cli()