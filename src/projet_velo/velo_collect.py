import csv
from datetime import datetime, timedelta
from pathlib import Path
import re
import time
import requests

from .functions import fetch_station_status, load_config

CSV_HEADER = [
    "timestamp",
    "station_id",
    "bikes",
    "docks",
    "is_installed",
    "is_renting",
    "is_returning",
    "last_reported",
]


def _parse_end_time(args, start_time: datetime) -> datetime | None:
    """Calcule la date/heure d'arrêt à partir de --duration ou --until."""
    if args.duration:
        match = re.fullmatch(r"(\d+)([hms])", args.duration.strip().lower())
        if not match:
            raise ValueError("Format de durée invalide (exemples : 3h, 90m, 120s).")
        val, unit = int(match.group(1)), match.group(2)
        if unit == "h":
            return start_time + timedelta(hours=val)
        if unit == "m":
            return start_time + timedelta(minutes=val)
        return start_time + timedelta(seconds=val)

    if args.until:
        try:
            target = datetime.strptime(args.until, "%Y-%m-%d %H:%M").astimezone()
        except ValueError:
            raise ValueError('Format de date invalide. Attendu : "AAAA-MM-JJ HH:MM".')
        if target <= start_time:
            raise ValueError("La date --until doit être postérieure à l'heure actuelle.")
        return target

    return None


def _save_snapshot(history_dir: Path, now_local: datetime, stations: list[dict]) -> None:
    """Enregistre un relevé dans le fichier CSV correspondant à la date locale."""
    history_dir.mkdir(parents=True, exist_ok=True)
    csv_path = history_dir / f"{now_local.strftime('%Y-%m-%d')}.csv"
    file_exists = csv_path.is_file()

    ts_iso = now_local.isoformat(timespec="seconds")

    with open(csv_path, "a", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(CSV_HEADER)

        for s in stations:
            last_rep_ts = s.get("last_reported")
            if last_rep_ts:
                last_rep_iso = (
                    datetime.fromtimestamp(last_rep_ts)
                    .astimezone()
                    .isoformat(timespec="seconds")
                )
            else:
                last_rep_iso = ts_iso

            writer.writerow([
                ts_iso,
                s["station_id"],
                s.get("num_bikes_available", 0),
                s.get("num_docks_available", 0),
                str(bool(s.get("is_installed", False))).lower(),
                str(bool(s.get("is_renting", False))).lower(),
                str(bool(s.get("is_returning", False))).lower(),
                last_rep_iso,
            ])


def handle_collect(args) -> int:
    """Point d'entrée de la commande `velo collect`."""
    config = load_config()

    interval = (
        args.interval
        if args.interval is not None
        else config.get("collect", {}).get("interval_seconds", 120)
    )
    if interval < 60:
        print(f"Erreur : l'intervalle minimum est de 60 secondes (reçu : {interval}).")
        return 1

    start_time = datetime.now().astimezone()
    try:
        end_time = _parse_end_time(args, start_time)
    except ValueError as e:
        print(f"Erreur : {e}")
        return 1

    gbfs_url = config["network"]["gbfs_url"]
    history_dir = Path(config["data"]["folder"]) / "vlille" / "history"

    last_seen_updated: int | None = None
    snapshots_count = 0
    first_snap_time: datetime | None = None
    last_snap_time: datetime | None = None

    print("Démarrage de la collecte (Ctrl+C pour arrêter)...")

    try:
        while True:
            now = datetime.now().astimezone()
            if end_time and now >= end_time:
                break

            try:
                last_updated, stations = fetch_station_status(gbfs_url)

                if last_updated == last_seen_updated:
                    print(f"[{now.strftime('%H:%M:%S')}] Relevé ignoré (données inchangées).")
                else:
                    _save_snapshot(history_dir, now, stations)
                    last_seen_updated = last_updated
                    snapshots_count += 1
                    if first_snap_time is None:
                        first_snap_time = now
                    last_snap_time = now
                    print(
                        f"[{now.strftime('%H:%M:%S')}] Relevé #{snapshots_count} enregistré ({len(stations)} stations)."
                    )

            except (requests.RequestException, KeyError, ValueError, RuntimeError, OSError) as e:
                print(
                    f"[{now.strftime('%H:%M:%S')}] Erreur lors de la collecte : {e} (nouvel essai au prochain cycle)"
                )

            if args.once:
                break

            sleep_seconds = float(interval)
            if end_time:
                remaining = (end_time - datetime.now().astimezone()).total_seconds()
                if remaining <= 0:
                    break
                sleep_seconds = min(sleep_seconds, remaining)

            time.sleep(sleep_seconds)

    except KeyboardInterrupt:
        print("\nArrêt demandé par l'utilisateur.")

    debut_str = first_snap_time.strftime("%d/%m/%Y %H:%M:%S") if first_snap_time else "aucun"
    fin_str = last_snap_time.strftime("%d/%m/%Y %H:%M:%S") if last_snap_time else "aucun"
    print(f"Bilan : {snapshots_count} relevé(s) | Début : {debut_str} | Fin : {fin_str}")
    return 0