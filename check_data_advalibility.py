import argparse
import json
import logging
import os
from random import randint
from datetime import datetime

import numpy as np

# import time
import pandas as pd
from tqdm import tqdm

from parse_statsbomb_data import (
    get_json_from_web_gz,
    get_list_of_statsbomb_games,
    parse_statsbomb_amf_tracking_data,
)


def check_data_advalibility(
    check_csv: bool = False,
    check_parquet: bool = False,
    check_all_seasons: bool = True
):
    if check_csv is False and check_parquet is False:
        raise ValueError(
            "Please specify if you want to check the `.csv` files" +
            ", or the `.parquet` files."
        )

    games_df = get_list_of_statsbomb_games()

    if check_all_seasons is False:
        seasons_arr = games_df["season"].to_numpy()
        seasons_arr = np.unique(seasons_arr)
        s_len = len(seasons_arr)-1
        s = seasons_arr[randint(0, s_len)]
        games_df = games_df[games_df["season"] == s]

        del seasons_arr, s_len, s

    game_ids_arr = games_df["nfl_game_id"].to_numpy()
    url_arr = games_df["url"].to_numpy()

    for i in tqdm(range(0, len(game_ids_arr))):
        game_id = game_ids_arr[i]
        game_url = url_arr[i]
        print(f"\nChecking game {game_id}")
        if check_csv is True:
            try:
                df = pd.read_csv(
                    "https://github.com/sportsdataverse/" +
                    "amf-location-data/releases/download/" +
                    f"amf_tracking_csv/{game_id}.csv"
                )
                print(df)
                print(f"\n{game_id} is verified to to exist in `.csv` form.")

            except Exception as e:
                logging.warning(
                    f"NFL game ID #{game_id} could not be reached.\n"
                    + f"Unhandled exception: {e}"
                )
                logging.info("Attempting to re-download this game.")

                json_data = get_json_from_web_gz(game_url)
                parsed_df = parse_statsbomb_amf_tracking_data(json_data)
                parsed_df.to_csv(f"statsbomb/{game_id}.csv", index=False)

        elif check_parquet is True:
            try:
                df = pd.read_parquet(
                    "https://github.com/sportsdataverse/" +
                    "amf-location-data/releases/download/" +
                    f"amf_tracking_parquet/{game_id}.parquet"
                )
                print(df)
                print(
                    f"\n{game_id} is verified to to exist in `.parquet` form."
                )

            except Exception as e:
                logging.warning(
                    f"NFL game ID #{game_id} could not be reached.\n"
                    + f"Unhandled exception: {e}"
                )
                logging.info("Attempting to re-download this game.")
                json_data = get_json_from_web_gz(game_url)
                parsed_df = parse_statsbomb_amf_tracking_data(json_data)
                parsed_df.to_parquet(
                    f"statsbomb/{game_id}.parquet",
                    index=False
                )

        del game_id, game_url


if __name__ == "__main__":
    now = datetime.now()
    check_all_seasons = False

    if now.day <= 8:
        check_all_seasons = True

    try:
        os.mkdir("statsbomb")
    except Exception as e:
        logging.info(f"Unhandled exception: {e}")

    parser = argparse.ArgumentParser()
    parser.add_argument("-csv", action="store_true")
    parser.add_argument("-parquet", action="store_true")

    args = parser.parse_args()

    csv_flag = args.csv
    parquet_flag = args.parquet

    if csv_flag is True and parquet_flag is True:
        raise ValueError(
            "Please specify if you want to check the `.csv` " +
            "files, or the `.parquet` files."
        )
    elif csv_flag is True:
        check_data_advalibility(
            check_csv=True,
            check_all_seasons=check_all_seasons
        )
    elif parquet_flag is True:
        check_data_advalibility(
            check_parquet=True,
            check_all_seasons=check_all_seasons
        )

    timestamp_json = {
        "last_check": {"month": now.month, "day": now.day, "year": now.year},
        "check_all_seasons": check_all_seasons,
        "check_csv": csv_flag,
        "check_parquet": parquet_flag,
    }

    with open("statsbomb/last_check_timestamp.json", "w+") as f:
        f.write(json.dumps(timestamp_json))
