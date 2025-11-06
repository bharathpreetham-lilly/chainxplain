"""
ChainXplain CLI - Command-line interface for blockchain analysis.

Beautiful terminal interface for analyzing contracts, wallets, and transactions.
"""

import sys
from typing import Optional
import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.markdown import Markdown
from rich import print as rprint
from rich.progress import Progress, SpinnerColumn, TextColumn

from chainxplain.client import ChainExplainClient
from chainxplain.config import load_settings


# Create Typer app
app = typer.Typer(
    name="chainxplain",
    help="🔗 AI-powered blockchain contract and wallet analyzer",
    add_completion=False,
)

# Rich console for beautiful output
console = Console()


def get_client() -> ChainExplainClient:
    """Get or create ChainXplain client."""
    try:
        settings = load_settings()
        return ChainExplainClient(settings=settings)
    except ValueError as e:
        console.print(f"[red]❌ Error:[/red] {e}")
        console.print("\n[yellow]Please configure your API keys in .env file:[/yellow]")
        console.print("  ANTHROPIC_API_KEY=your-key-here")
        console.print("  ETHERSCAN_API_KEY=your-key-here")
        sys.exit(1)


@app.command("explain")
def explain_contract(
    address: str = typer.Argument(..., help="Contract address to analyze"),
    chain: str = typer.Option("ethereum", "--chain", "-c", help="Blockchain network"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Show detailed output"),
):
    """
    🔍 Analyze and explain a smart contract.
    
    Provides AI-powered analysis of what the contract does, its risks,
    and key functionality.
    
    Example:
        chainxplain explain 0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48 --chain ethereum
    """
    console.print(f"\n[bold cyan]🔍 Analyzing contract on {chain}...[/bold cyan]\n")
    
    client = get_client()
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("Fetching contract data...", total=None)
        
        try:
            result = client.analyze_contract(address=address, chain=chain)
            progress.update(task, description="✅ Analysis complete!")
        except Exception as e:
            progress.stop()
            console.print(f"[red]❌ Error:[/red] {e}")
            sys.exit(1)
    
    # Display results
    console.print()
    console.print(Panel(
        f"[bold]{result.name or 'Unknown Contract'}[/bold]",
        title="📄 Contract",
        border_style="cyan",
    ))
    
    # Risk level with color
    risk_colors = {
        "low": "green",
        "medium": "yellow",
        "high": "red",
        "critical": "red bold",
    }
    risk_color = risk_colors.get(result.risk_level.lower(), "white")
    
    console.print(f"\n[bold]Risk Level:[/bold] [{risk_color}]{result.risk_level.upper()}[/{risk_color}]")
    console.print(f"[bold]Chain:[/bold] {chain}")
    console.print(f"[bold]Address:[/bold] [dim]{address}[/dim]")
    
    if result.is_verified:
        console.print("[green]✅ Contract is verified[/green]")
    else:
        console.print("[yellow]⚠️  Contract is not verified[/yellow]")
    
    # Summary
    console.print(f"\n[bold cyan]📝 Summary:[/bold cyan]")
    console.print(Panel(result.summary, border_style="blue"))
    
    # Token info
    if result.token_info:
        console.print(f"\n[bold cyan]🪙 Token Information:[/bold cyan]")
        token_table = Table(show_header=False, box=None)
        token_table.add_column("Property", style="cyan")
        token_table.add_column("Value")
        
        for key, value in result.token_info.items():
            token_table.add_row(key.replace("_", " ").title(), str(value))
        
        console.print(token_table)
    
    # Key functions
    if result.key_functions:
        console.print(f"\n[bold cyan]⚙️  Key Functions:[/bold cyan]")
        for func in result.key_functions[:10]:  # Show top 10
            console.print(f"  • {func}")
    
    # Detailed analysis (verbose mode)
    if verbose and result.detailed_analysis:
        console.print(f"\n[bold cyan]📊 Detailed Analysis:[/bold cyan]")
        console.print(Panel(
            Markdown(result.detailed_analysis),
            border_style="green",
        ))
    
    console.print()


@app.command("wallet")
def analyze_wallet_cmd(
    address: str = typer.Argument(..., help="Wallet address to analyze"),
    chain: str = typer.Option("ethereum", "--chain", "-c", help="Blockchain network"),
    limit: int = typer.Option(50, "--limit", "-l", help="Number of recent transactions"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Show detailed output"),
):
    """
    💰 Analyze wallet activity and transaction history.
    
    Provides comprehensive analysis of wallet transactions, holdings,
    and activity patterns.
    
    Example:
        chainxplain wallet 0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb --limit 100
    """
    console.print(f"\n[bold cyan]💰 Analyzing wallet on {chain}...[/bold cyan]\n")
    
    client = get_client()
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task(f"Fetching last {limit} transactions...", total=None)
        
        try:
            result = client.analyze_wallet(address=address, chain=chain, limit=limit)
            progress.update(task, description="✅ Analysis complete!")
        except Exception as e:
            progress.stop()
            console.print(f"[red]❌ Error:[/red] {e}")
            sys.exit(1)
    
    # Display results
    console.print()
    console.print(Panel(
        f"[bold]Wallet Analysis[/bold]",
        title="💼 Wallet",
        border_style="cyan",
    ))
    
    console.print(f"\n[bold]Address:[/bold] [dim]{address}[/dim]")
    console.print(f"[bold]Chain:[/bold] {chain}")
    console.print(f"[bold]Total Transactions:[/bold] {result.total_transactions:,}")
    
    # Token holdings
    if result.token_holdings:
        console.print(f"\n[bold cyan]🪙 Token Holdings:[/bold cyan]")
        holdings_table = Table()
        holdings_table.add_column("Token", style="cyan")
        holdings_table.add_column("Balance", justify="right")
        holdings_table.add_column("Value (USD)", justify="right")
        
        for holding in result.token_holdings[:20]:  # Top 20
            holdings_table.add_row(
                holding.get("symbol", "Unknown"),
                f"{holding.get('balance', 0):.4f}",
                f"${holding.get('value_usd', 0):.2f}" if holding.get('value_usd') else "N/A"
            )
        
        console.print(holdings_table)
    
    # Recent activity
    if result.recent_activity:
        console.print(f"\n[bold cyan]📊 Recent Activity:[/bold cyan]")
        activity_table = Table()
        activity_table.add_column("Type", style="cyan")
        activity_table.add_column("Details")
        activity_table.add_column("Time", style="dim")
        
        for activity in result.recent_activity[:10]:  # Last 10
            activity_table.add_row(
                activity.get("type", "Unknown"),
                activity.get("description", "N/A"),
                activity.get("timestamp", "N/A")
            )
        
        console.print(activity_table)
    
    # Summary
    console.print(f"\n[bold cyan]📝 Summary:[/bold cyan]")
    console.print(Panel(result.summary, border_style="blue"))
    
    # Insights (verbose mode)
    if verbose and result.insights:
        console.print(f"\n[bold cyan]💡 Insights:[/bold cyan]")
        for insight in result.insights:
            console.print(f"  • {insight}")
    
    console.print()


@app.command("tx")
def analyze_transaction(
    tx_hash: str = typer.Argument(..., help="Transaction hash to analyze"),
    chain: str = typer.Option("ethereum", "--chain", "-c", help="Blockchain network"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Show detailed output"),
):
    """
    🔄 Analyze a specific transaction.
    
    Provides human-readable explanation of what happened in a transaction.
    
    Example:
        chainxplain tx 0xabc123... --chain ethereum
    """
    console.print(f"\n[bold cyan]🔄 Analyzing transaction on {chain}...[/bold cyan]\n")
    
    client = get_client()
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("Fetching transaction data...", total=None)
        
        try:
            result = client.analyze_transaction(tx_hash=tx_hash, chain=chain)
            progress.update(task, description="✅ Analysis complete!")
        except Exception as e:
            progress.stop()
            console.print(f"[red]❌ Error:[/red] {e}")
            sys.exit(1)
    
    # Display results
    console.print()
    console.print(Panel(
        f"[bold]Transaction Details[/bold]",
        title="🔄 Transaction",
        border_style="cyan",
    ))
    
    # Status
    status_icon = "✅" if result.status == "success" else "❌"
    status_color = "green" if result.status == "success" else "red"
    
    console.print(f"\n[bold]Status:[/bold] [{status_color}]{status_icon} {result.status.upper()}[/{status_color}]")
    console.print(f"[bold]Hash:[/bold] [dim]{tx_hash}[/dim]")
    console.print(f"[bold]From:[/bold] [dim]{result.from_address}[/dim]")
    console.print(f"[bold]To:[/bold] [dim]{result.to_address}[/dim]")
    console.print(f"[bold]Value:[/bold] {result.value} ETH")
    console.print(f"[bold]Gas Used:[/bold] {result.gas_used:,}")
    console.print(f"[bold]Gas Price:[/bold] {result.gas_price} Gwei")
    
    # Explanation
    console.print(f"\n[bold cyan]📝 What Happened:[/bold cyan]")
    console.print(Panel(result.explanation, border_style="blue"))
    
    # Contract calls (verbose mode)
    if verbose and result.contract_calls:
        console.print(f"\n[bold cyan]📞 Contract Calls:[/bold cyan]")
        for call in result.contract_calls:
            console.print(f"  • {call}")
    
    # Events (verbose mode)
    if verbose and result.events:
        console.print(f"\n[bold cyan]📡 Events Emitted:[/bold cyan]")
        for event in result.events:
            console.print(f"  • {event}")
    
    console.print()


@app.command("token")
def get_token_info_cmd(
    address: str = typer.Argument(..., help="Token contract address"),
    chain: str = typer.Option("ethereum", "--chain", "-c", help="Blockchain network"),
):
    """
    🪙 Get information about a token contract.
    
    Shows token metadata, supply, and basic details.
    
    Example:
        chainxplain token 0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48
    """
    console.print(f"\n[bold cyan]🪙 Fetching token info on {chain}...[/bold cyan]\n")
    
    client = get_client()
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("Fetching token data...", total=None)
        
        try:
            result = client.analyze_contract(address=address, chain=chain)
            progress.update(task, description="✅ Done!")
        except Exception as e:
            progress.stop()
            console.print(f"[red]❌ Error:[/red] {e}")
            sys.exit(1)
    
    # Display results
    console.print()
    console.print(Panel(
        f"[bold]{result.name or 'Unknown Token'}[/bold]",
        title="🪙 Token",
        border_style="cyan",
    ))
    
    if result.token_info:
        info_table = Table(show_header=False, box=None)
        info_table.add_column("Property", style="cyan bold")
        info_table.add_column("Value")
        
        for key, value in result.token_info.items():
            info_table.add_row(key.replace("_", " ").title(), str(value))
        
        console.print(info_table)
    
    console.print(f"\n[bold cyan]📝 Description:[/bold cyan]")
    console.print(Panel(result.summary, border_style="blue"))
    console.print()


@app.command("version")
def show_version():
    """Show ChainXplain version."""
    from chainxplain import __version__
    console.print(f"\n[bold cyan]ChainXplain[/bold cyan] version [green]{__version__}[/green]\n")


@app.callback()
def callback():
    """
    ChainXplain - AI-powered blockchain analysis.
    
    Analyze smart contracts, wallets, and transactions with AI-powered explanations.
    """
    pass


if __name__ == "__main__":
    app()
