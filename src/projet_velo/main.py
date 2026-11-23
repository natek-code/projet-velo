import argparse
from .velo_init import handle_init
from .refresh import handle_refresh
from .velo_station import handle_station_list, handle_station_search
from .velo_favorites import handle_favorites, handle_favorites_add, handle_favorites_remove

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="velo",
        description="Outil en ligne de commande pour consulter et analyser les réseaux GBFS (défaut : V'Lille).",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # velo init [--force]
    init_p = subparsers.add_parser("init", help="Initialise configuration, dossiers et données")
    init_p.add_argument("--force", action="store_true", help="Ecrase la configuration existante")

    # velo refresh
    subparsers.add_parser("refresh", help="Met à jour les données statiques du réseau")

    # velo status
    subparsers.add_parser("status", help="Résumé de l'état du réseau en temps réel")

    # velo station {search <texte> | list}
    station_p = subparsers.add_parser("station", help="Consulter ou chercher des stations")
    station_sub = station_p.add_subparsers(dest="station_action", required=True)

    search_p = station_sub.add_parser("search", help="Rechercher une station par expression régulière")
    search_p.add_argument("texte", help="Motif ou texte recherché dans le nom")

    station_sub.add_parser("list", help="Lister toutes les stations")

    # velo favorites [{add <id> | remove <id>}]
    fav_p = subparsers.add_parser("favorites", help="Gérer et afficher les stations favorites")
    fav_sub = fav_p.add_subparsers(dest="favorites_action")

    fav_add = fav_sub.add_parser("add", help="Ajouter une station aux favoris")
    fav_add.add_argument("station_id", help="Identifiant de la station")

    fav_rem = fav_sub.add_parser("remove", help="Retirer une station des favoris")
    fav_rem.add_argument("station_id", help="Identifiant de la station")

    # velo alerts [--low-bikes N] [--low-docks N]
    alerts_p = subparsers.add_parser("alerts", help="Lister les alertes sur les stations")
    alerts_p.add_argument("--low-bikes", type=int, default=None, help="Seuil vélos (vide/presque vide)")
    alerts_p.add_argument("--low-docks", type=int, default=None, help="Seuil places libres (pleine/presque pleine)")

    # velo dashboard [--refresh SECONDES]
    dash_p = subparsers.add_parser("dashboard", help="Tableau de bord mis à jour en continu")
    dash_p.add_argument("--refresh", type=int, default=None, help="Intervalle de rafraîchissement en secondes")

    # velo collect [--interval SECONDES] (--duration DUREE | --until "..." | --once)
    collect_p = subparsers.add_parser("collect", help="Collecter l'historique à intervalle régulier")
    collect_p.add_argument("--interval", type=int, default=None, help="Intervalle entre relevés en secondes")

    stop_group = collect_p.add_mutually_exclusive_group()
    stop_group.add_argument("--duration", type=str, default=None, help="Durée avant arrêt (ex. : 3h, 90m)")
    stop_group.add_argument("--until", type=str, default=None, help='Arrêt à une date/heure ("AAAA-MM-JJ HH:MM")')
    stop_group.add_argument("--once", action="store_true", help="Effectuer un seul relevé puis s'arrêter")

    # velo history [--from AAAA-MM-JJ] [--to AAAA-MM-JJ]
    history_p = subparsers.add_parser("history", help="Afficher les périodes collectées")
    history_p.add_argument("--from", dest="date_from", type=str, default=None, help="Date de début (AAAA-MM-JJ)")
    history_p.add_argument("--to", dest="date_to", type=str, default=None, help="Date de fin (AAAA-MM-JJ)")

    # velo query-metric METRIQUE [METRIQUE ...] [sélection] [--by GROUPE] [--top N]
    query_p = subparsers.add_parser("query-metric", help="Analyser l'historique collecté")
    query_p.add_argument(
        "metrics",
        nargs="+",
        choices=["avg_bikes", "avg_docks", "empty_rate", "full_rate"],
        help="Une ou plusieurs métriques à calculer",
    )
    query_p.add_argument("--date", type=str, default=None, help="Jour précis (AAAA-MM-JJ)")
    query_p.add_argument("--from", dest="date_from", type=str, default=None, help="Début de plage")
    query_p.add_argument("--to", dest="date_to", type=str, default=None, help="Fin de plage")
    query_p.add_argument("--period", nargs="+", type=int, default=None, help="Numéro(s) de période")
    query_p.add_argument("--days", type=str, default=None, help="weekdays, weekend ou liste de jours")
    query_p.add_argument("--hours", type=str, default=None, help="Plage horaire (ex. : 7-9)")
    query_p.add_argument("--station", type=str, default=None, help="Identifiant d'une station")
    query_p.add_argument(
        "--by",
        choices=["station", "hour", "weekday", "day"],
        default=None,
        help="Regroupement des résultats",
    )
    query_p.add_argument("--top", type=int, default=None, help="Limiter aux N premiers résultats")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    match args.command:
        case "init":
            return handle_init(args)
        case "refresh":
            return handle_refresh(args)
        case "status":
            return handle_status(args)
        case "station":
            match args.station_action:
                case "search":
                    return handle_station_search(args)
                case "list":
                    return handle_station_list(args)
                case _:
                    return 1
        case "favorites":
            match args.favorites_action:
                case "add":
                    return handle_favorites_add(args)
                case "remove":
                    return handle_favorites_remove(args)
                case None:
                    return handle_favorites(args)
                case _:
                    return 1
        case "alerts":
            return handle_alerts(args)
        case "dashboard":
            return handle_dashboard(args)
        case "collect":
            return handle_collect(args)
        case "history":
            return handle_history(args)
        case "query-metric":
            return handle_query_metric(args)
        case _:
            return 1


if __name__ == "__main__":
    main()