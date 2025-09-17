import click
import logic
from pprint import pprint

def get_multiline_input(prompt):
    """Helper function to get multiline input from the user."""
    click.echo(f"\n{prompt}")
    click.echo("(Finish with Ctrl+D on Unix or Ctrl+Z+Enter on Windows)")
    lines = []
    while True:
        try:
            line = input()
            lines.append(line)
        except EOFError:
            break
    return "\n".join(lines)

@click.group()
def cli():
    """A CLI tool to help generate company names."""
    pass

@cli.command()
def start():
    """Starts the interactive process to generate a company name."""
    click.echo(click.style("Welcome to the Company Name Generator CLI!", fg='cyan', bold=True))
    click.echo("This tool will guide you through a few steps to generate a great name for your company.")

    # --- Step 1: Gather Initial Data ---
    click.echo(click.style("\n--- Step 1: Tell us about your company ---", fg='yellow'))
    data = {}
    data['headline'] = click.prompt("Enter the headline for your company")
    data['what'] = get_multiline_input("Describe what your company offers (2-3 sentences)")
    data['forWho'] = get_multiline_input("Describe your target audience")
    data['features'] = get_multiline_input("List 3-5 key features or benefits")

    # --- Step 2: Generate and Validate UVP ---
    click.echo(click.style("\n--- Step 2: Generating Unique Value Proposition (UVP) ---", fg='yellow'))
    try:
        with click.progressbar(length=100, label='Thinking...') as bar:
            for i in range(100):
                # This is just for visual effect, the real work is next
                pass
        uvp = logic.generate_uvp(data)
        click.echo(click.style("\nHere is your generated UVP:", fg='green'))
        click.echo(f"> {uvp}")

        if click.confirm("\nDo you want to edit this UVP?", default=False):
            edited_uvp = click.edit(uvp)
            data['uvp'] = edited_uvp.strip() if edited_uvp else uvp
        else:
            data['uvp'] = uvp

    except Exception as e:
        click.echo(click.style(f"\nError generating UVP: {e}", fg='red'))
        return

    # --- Step 3: Generate and Curate Lexicon ---
    click.echo(click.style("\n--- Step 3: Generating Lexicon ---", fg='yellow'))
    try:
        with click.progressbar(length=100, label='Brainstorming words...') as bar:
            for i in range(100):
                pass
        lexicon = logic.generate_lexicon(data)
        click.echo(click.style(f"\nWe have generated {len(lexicon)} words for your lexicon.", fg='green'))

        if click.confirm("\nDo you want to curate the lexicon? (You'll be asked to keep/discard each word)", default=True):
            words_to_keep = []
            for item in lexicon:
                if click.confirm(f"Keep '{item['word']}'? ({item['relevance']})", default=True):
                    words_to_keep.append(item)
            data['lexicon'] = words_to_keep
            click.echo(click.style(f"\nLexicon curated. You kept {len(words_to_keep)} words.", fg='green'))
        else:
            data['lexicon'] = lexicon

    except Exception as e:
        click.echo(click.style(f"\nError generating lexicon: {e}", fg='red'))
        return

    # --- Step 4: Generate Names ---
    click.echo(click.style("\n--- Step 4: Generating Company Names ---", fg='yellow'))
    try:
        with click.progressbar(length=100, label='Coming up with names...') as bar:
            for i in range(100):
                pass
        names = logic.generate_and_check_names(data)
        click.echo(click.style("\nHere are your generated company names:", fg='green', bold=True))

        for name_info in names:
            name = name_info['name']
            domain_status = "Available" if name_info['domainAvailable'] else "Unavailable"
            color = "green" if name_info['domainAvailable'] else "red"
            competitors = name_info['competitors']

            click.echo(f"\n- Name: {click.style(name, bold=True)}")
            click.echo(f"  .com Domain: {click.style(domain_status, fg=color)}")
            click.echo(f"  Potential Competitors: {competitors}")

    except Exception as e:
        click.echo(click.style(f"\nError generating names: {e}", fg='red'))
        return

    click.echo(click.style("\nProcess complete!", fg='cyan', bold=True))

if __name__ == '__main__':
    cli()
