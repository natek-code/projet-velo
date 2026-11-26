
import requests
from .velo_status import *
from .functions import *

from rich import print
from rich.panel import Panel
from rich.align import Align

from rich.layout import Layout



def handle_dashboard(args):
    config = load_config()
    gbfs_url = config["network"]["gbfs_url"]
    network_name = config["network"]["name"]
   
    resultat = calcul_status()
    Header = Align.center(f"{network_name} - données du [blue]{resultat["maintenant"]:%d/%m/%Y}[/blue] à [green]{resultat["maintenant"]:%H:%M:%S}[/green]")
    
    Info = Align.center(f"Stations en service: {resultat["marche"]} / {resultat["nombre"]} \nHors service: {resultat["nombre"]-resultat["marche"]} \nVides {resultat["vide"]} \nPleines: {resultat["plein"]} \nTaux de remplissage {round((resultat["velos"]/resultat["places"])*100)}%")

    layout = Layout()

    layout.split_column(Layout(name="upper", size=3),Layout(name="middle"), Layout(name="lower"))
    layout["middle"].split_row(Layout(name="left"),Layout(name="right"))

    layout["upper"].update(Panel(Header))
    layout["middle"]["left"].update(Panel(Info))
    print(layout)

   



   


if __name__ == "__main__":
    handle_dashboard()