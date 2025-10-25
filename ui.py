"""
    using rich for a ui
"""

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress
from rich import box

console = Console()


"""     MESSAGE STYLING BELOW       """
def print_header(text: str):
    """prints a styled header"""
    console.print(f"\n[bold cyan]{text}[/bold cyan]")
    console.print("-" * 50)
def print_success(text: str):
    """prints a styled success message"""
    console.print(f"✓ [green]{text}[/green]")
def print_error(text: str):
    """prints a styled error message"""
    console.print(f"✗ [red]{text}[/red]")
def print_warning(text: str):
    """prints a styled warning message"""
    console.print(f"!!!   [green]{text}[/green]   !!!")
def print_info(text: str):
    """prints a styled warning message"""
    console.print(f"[cyan]{text}[/cyan]")

"""     PASSWORD LIST TABLE BELOW       """
def display_password_list(entries: list, show_passwords: bool = False):
    """
    Display passwords in a beautiful table.
    
    Args:
        entries: List of password entries
        show_passwords: Whether to show actual passwords (default: hide)
    """
    if not entries:
        print_warning("No passwords stored yet!")
        return
    
    table = Table(title="🔐 Stored Passwords", box=box.ROUNDED)
    
    table.add_column("#", style="cyan", width=4)
    table.add_column("Service", style="magenta", width=20)
    table.add_column("Username", style="blue", width=25)
    table.add_column("Strength", style="yellow", width=12)
    table.add_column("Created", style="green", width=12)
    
    for i, entry in enumerate(entries, 1):
        strength = entry.get('strength', 'unknown').upper()
        
        # Color code strength
        if 'very strong' in strength.lower():
            strength_colored = f"[bold green]{strength}[/bold green]"
        elif 'strong' in strength.lower():
            strength_colored = f"[green]{strength}[/green]"
        elif 'medium' in strength.lower():
            strength_colored = f"[yellow]{strength}[/yellow]"
        else:
            strength_colored = f"[red]{strength}[/red]"
        
        table.add_row(
            str(i),
            entry['service'],
            entry['username'],
            strength_colored,
            entry['created']
        )
    
    console.print(table)

"""     PASSWORD INFO BELOW       """

def display_password_info(entry: dict, decrypted_password: str, strength_result: dict):
    # Color code strength
    score = strength_result['score']
    rating = strength_result['rating'].upper()
    
    if score >= 80:
        strength_color = "bold green"
    elif score >= 60:
        strength_color = "green"
    elif score >= 40:
        strength_color = "yellow"
    else:
        strength_color = "red"
    
    # Build info text
    info_text = f"""
[bold cyan]Service:[/bold cyan]  {entry['service']}
[bold cyan]Username:[/bold cyan] {entry['username']}
[bold cyan]Password:[/bold cyan] {decrypted_password}
[bold cyan]Created:[/bold cyan]  {entry['created']}
[bold cyan]Strength:[/bold cyan] [{strength_color}]{rating} ({score}/100)[/{strength_color}]
"""
    
    panel = Panel(
        info_text.strip(),
        title="🔓 Password Information",
        border_style="cyan",
        box=box.DOUBLE
    )
    
    console.print(panel)

"""     STRENGTH ANALYSIS (and feedback)BELOW       """
def display_strength_bar(score: int, rating: str):
    # Determine color
    if score >= 80:
        color = "green"
    elif score >= 60:
        color = "yellow"
    elif score >= 40:
        color = "orange1"
    else:
        color = "red"
    
    # Create bar (20 chars wide)
    filled = int(score / 5)  # 100 / 5 = 20 chars
    bar = "█" * filled + "░" * (20 - filled)
    
    console.print(f"\n[bold]Strength:[/bold] [{color}]{bar}[/{color}] {score}/100 ({rating.upper()})")

def display_feedback(feedback_list: list):
    """
    Display password improvement feedback.
    
    Args:
        feedback_list: List of feedback strings
    """
    if not feedback_list:
        return
    
    console.print("\n[bold yellow]💡 Suggestions:[/bold yellow]")
    for item in feedback_list:
        console.print(f"  {item}")

"""     MAIN MENU BELOW       """
def display_main_menu():
    """Display the main menu"""
    menu_panel = Panel(
        """[bold cyan]1.[/bold cyan] Add a new password
[bold cyan]2.[/bold cyan] Retrieve a password
[bold cyan]3.[/bold cyan] Update a password
[bold cyan]4.[/bold cyan] Delete a password
[bold cyan]5.[/bold cyan] Analyze password strength
[bold cyan]6.[/bold cyan] Exit""",
        title="🔐 PASSWORD MANAGER",
        border_style="green",
        box=box.DOUBLE
    )
    console.print(menu_panel)