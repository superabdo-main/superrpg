

def tier_design(tier):
    if tier == "I":
        return "[white]I[/white]"
    elif tier == "II":
        return "[yellow]II[/yellow]"
    elif tier == "III":
        return "[blue]III[/blue]"
    elif tier == "IV":
        return "[orange]IV[/orange]"
    elif tier == "V":
        return "[red]V[/red]"
    else:
        return "[red]Unknown[/red]"