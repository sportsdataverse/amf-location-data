import json
import logging
import os
from datetime import datetime
from gzip import decompress
from math import atan2, degrees, sqrt

import pandas as pd
import requests
from tqdm import tqdm


def get_angle_from_two_points(
    point_1_x: float, point_1_y: float, point_2_x: float, point_2_y: float
):
    """ """
    # v1_theta = atan2(point_1_y, point_1_x)
    # v2_theta = atan2(point_2_y, point_2_x)
    # r = (v2_theta - v1_theta) * (180.0 / np.pi)
    # if r < 0:
    #     r % 360

    # return r
    angle = degrees(atan2(point_1_y - point_2_y, point_1_x - point_2_x))
    if angle < 0:
        angle += 360

    return angle


def get_distance_from_two_points(
    point_1_x: float, point_1_y: float, point_2_x: float, point_2_y: float
):
    """ """
    x = (point_2_x - point_1_x) ** 2
    y = (point_2_y - point_1_y) ** 2

    dist = sqrt(x + y)
    return dist


def get_json_from_web_gz(url: str):
    """ """
    user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) " + \
        "AppleWebKit/537.36 (KHTML, like Gecko) " + \
        "Chrome/83.0.4103.97 Safari/537.36"
    headers = {
        "User-Agent": user_agent
    }
    logging.info(f"Getting data from url `{url}`")
    logging.info("Attempting to download data and hold the data in memory.")
    response = requests.get(url=url, headers=headers)

    if response.status_code == 200:
        logging.info("Data loaded successfully.")
    else:
        logging.critical(
            "Failed to download the data from the specified url. " +
            f"HTTP status code {response.status_code}."
        )
        raise ConnectionError(
            "Failed to download the data from the specified url. " +
            f"HTTP status code {response.status_code}."
        )

    logging.info(
        "Attempting to decompress the `.gz` file that was downloaded."
    )

    try:
        json_string = decompress(response.content)
        logging.info("Conversion from `.gz` to json object successful.")
    except Exception as e:
        logging.critical(f"Unhandled exception: {e}")
        raise RuntimeError(f"Unhandled exception: {e}")

    logging.info("Returning json data ")
    # print(json_string)

    return json.loads(json_string)


def get_list_of_statsbomb_games():
    """ """
    seasons = {}

    for i in range(1900, 2100):
        # In the final `seasons` dict,
        # it would look like this:
        # seasons["2000/2001"] = 2000
        seasons[f"{i}/{i+1}"] = i
    user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) " + \
        "AppleWebKit/537.36 (KHTML, like Gecko) " + \
        "Chrome/83.0.4103.97 Safari/537.36"
    headers = {
        "User-Agent": user_agent
    }
    url = (
        "https://raw.githubusercontent.com/" +
        "statsbomb/amf-open-data/main/data/games.json"
    )

    response = requests.get(url, headers=headers)
    json_data = json.loads(response.text)

    df = pd.json_normalize(json_data)

    df.replace({"season_name": seasons})
    df.rename(
        columns={
            "season_name": "season",
            "home_team.name": "home_team_name",
            "home_team.team_id": "home_team_id",
            "home_team.nfl_team_id": "home_team_abv",
            "away_team.name": "away_team_name",
            "away_team.team_id": "away_team_id",
            "away_team.nfl_team_id": "away_team_abv",
        },
        inplace=True,
    )
    return df


def parse_statsbomb_amf_tracking_data(json_data: dict):
    """ """
    tracking_df = pd.DataFrame()
    row_df = pd.DataFrame()

    df_columns = [
        "season",
        "season_id",
        "season_name",
        "game_id",
        "nfl_game_id",
        "nfl_old_game_id",
        "competition_id",
        "competition_name",
        "game_date",
        "play_quarter",
        "team_id",
        "nfl_team_id",
        "play_uuid",
        "gsis_play_id",
        "play_yardline",
        "offense_left_to_right",
        "play_direction",
        "game_clock",
        "player_id",
        "gsis_player_id",
        "position_code",
        "player_jersey_number",
        "player_name",
        "on_camera_ratio",
        "player_coverage_count",
        "calibration_fault_ratio",
        "track_id",
        "frame_num",
        "timestamp",
        "tracking_framerate",
        "time_since_last_frame",
        "play_start_timestamp",
        "play_end_timestamp",
        "player_start_timestamp",
        "player_end_timestamp",
        "time_since_snap",
        "x",
        "y",
        "ngs_x",
        "ngs_y",
        "player_speed",
        "player_acceleration",
        "player_distance",
        "player_orientation",
        "player_direction",
    ]

    game_id = json_data["game_id"]
    nfl_game_id = json_data["nfl_game_id"]
    nfl_old_game_id = json_data["nfl_old_game_id"]
    competition_name = json_data["competition_name"]
    competition_id = json_data["competition_id"]

    season_name = json_data["season_name"]
    season = int(season_name[0:4])

    season_id = json_data["season_id"]

    # "game_date": "2022-09-18",
    game_date_str = json_data["game_date"]
    game_date = datetime.strptime(game_date_str, "%Y-%m-%d")
    del game_date_str

    tracking_framerate = json_data["frequency"]

    logging.info(f"Parsing the tracking data from game ID #{game_id}")

    for play in tqdm(json_data["plays"]):
        play_uuid = play["play_uuid"]
        play_start_timestamp = play["start_timestamp"]
        play_end_timestamp = play["end_timestamp"]
        gsis_play_id = play["gsis_play_id"]
        play_quarter = play["play_quarter"]
        game_clock = play["game_clock"]
        play_yardline = play["play_yardline"]
        offense_left_to_right = play["offense_left_to_right"]
        player_coverage_count = play["player_coverage_count"]
        calibration_fault_ratio = play["calibration_fault_ratio"]

        for player in play["tracks"]:
            track_id = player["track_id"]
            try:
                player_start_timestamp = player["start_timestamp"]
            except Exception as e:
                logging.info(e)
                player_start_timestamp = None

            try:
                player_end_timestamp = player["end_timestamp"]
            except Exception as e:
                logging.info(e)
                play_end_timestamp = None

            team_id = player["team_id"]
            nfl_team_id = player["nfl_team_id"]
            player_id = player["player"]["player_id"]
            position_code = player["player"]["position_code"]
            player_name = player["player"]["name"]
            player_jersey_number = player["player"]["jersey_number"]
            gsis_player_id = player["player"]["gsis_player_id"]
            on_camera_ratio = player["on_camera_ratio"]

            row_df = pd.DataFrame(player["steps"])

            row_df["frame_num"] = row_df.reset_index().index

            row_df["play_uuid"] = play_uuid
            row_df["play_start_timestamp"] = play_start_timestamp
            row_df["play_end_timestamp"] = play_end_timestamp
            row_df["player_start_timestamp"] = player_start_timestamp
            row_df["player_end_timestamp"] = player_end_timestamp
            row_df["gsis_play_id"] = gsis_play_id
            row_df["play_quarter"] = play_quarter
            row_df["game_clock"] = game_clock
            row_df["play_yardline"] = play_yardline
            if offense_left_to_right is True:
                row_df["play_direction"] = "left"
            else:
                row_df["play_direction"] = "right"

            row_df["offense_left_to_right"] = offense_left_to_right
            row_df["player_coverage_count"] = player_coverage_count
            row_df["calibration_fault_ratio"] = calibration_fault_ratio
            row_df["track_id"] = track_id
            row_df["team_id"] = team_id
            row_df["nfl_team_id"] = nfl_team_id
            row_df["player_id"] = player_id
            row_df["gsis_player_id"] = gsis_player_id
            row_df["position_code"] = position_code
            row_df["player_jersey_number"] = player_jersey_number
            row_df["player_name"] = player_name
            row_df["on_camera_ratio"] = on_camera_ratio

            tracking_df = pd.concat([tracking_df, row_df], ignore_index=True)

            del row_df
            del track_id, player_start_timestamp, player_end_timestamp
            del team_id, nfl_team_id, player_id
            del position_code, player_name, player_jersey_number
            del gsis_player_id, on_camera_ratio

        del play_uuid, play_start_timestamp, play_end_timestamp
        del gsis_play_id, play_quarter
        del game_clock, play_yardline, offense_left_to_right
        del player_coverage_count, calibration_fault_ratio

    logging.info(
        "Applying NFL BDB-like columns to the tracking data in " +
        f"game ID #{game_id}"
    )
    tracking_df["season"] = season
    tracking_df["season_id"] = season_id
    tracking_df["season_name"] = season_name
    tracking_df["game_id"] = game_id
    tracking_df["nfl_game_id"] = nfl_game_id
    tracking_df["nfl_old_game_id"] = nfl_old_game_id
    tracking_df["competition_id"] = competition_id
    tracking_df["competition_name"] = competition_name
    tracking_df["game_date"] = game_date
    tracking_df["tracking_framerate"] = tracking_framerate

    # Calculate orientation and direction.
    tracking_df["x_lag_1"] = tracking_df.groupby(
        ["game_id", "track_id", "gsis_play_id"]
    )["x"].shift(1)
    tracking_df["y_lag_1"] = tracking_df.groupby(
        ["game_id", "track_id", "gsis_play_id"]
    )["y"].shift(1)

    tracking_df["x_lag_5"] = tracking_df.groupby(
        ["game_id", "track_id", "gsis_play_id"]
    )["x"].shift(5)
    tracking_df["y_lag_5"] = tracking_df.groupby(
        ["game_id", "track_id", "gsis_play_id"]
    )["y"].shift(5)

    tracking_df["time_since_last_frame"] = tracking_df[
        "time_since_snap"
    ] - tracking_df.groupby(["game_id", "track_id", "gsis_play_id"])[
        "time_since_snap"
    ].shift(
        1
    )
    tracking_df["speed_ref_time"] = tracking_df[
        "time_since_snap"
    ] - tracking_df.groupby(["game_id", "track_id", "gsis_play_id"])[
        "time_since_snap"
    ].shift(
        5
    )

    # Same as the `[dis]` column in the BDB dataset.
    tracking_df["player_distance"] = tracking_df.apply(
        lambda x: get_distance_from_two_points(
            x["x_lag_1"], x["y_lag_1"], x["x"], x["y"]
        ),
        axis=1,
    )
    tracking_df["speed_ref_dist"] = tracking_df.apply(
        lambda x: get_distance_from_two_points(
            x["x_lag_5"], x["y_lag_5"], x["x"], x["y"]
        ),
        axis=1,
    )

    # Same as the `[s]` column in the BDB dataset.
    # yds/s
    tracking_df["player_speed"] = (
        tracking_df["speed_ref_dist"] / tracking_df["speed_ref_time"]
    )

    # Same as the `[a]` column in the BDB dataset.
    # yds/s^2
    tracking_df["player_speed_lag_1"] = tracking_df.groupby(
        ["game_id", "track_id", "gsis_play_id"]
    )["player_speed"].shift(1)
    tracking_df["player_acceleration"] = (
        tracking_df["player_speed"] - tracking_df["player_speed_lag_1"]
    ) / tracking_df["time_since_last_frame"]

    # Same as the `[o]` column in the BDB dataset.
    # 5
    tracking_df["player_orientation"] = tracking_df.apply(
        lambda x: get_angle_from_two_points(
            x["x_lag_5"],
            x["y_lag_5"],
            x["x"],
            x["y"]
        ),
        axis=1,
    )

    # Same as the `[dir]` column in the BDB dataset.
    # 1
    tracking_df["player_direction"] = tracking_df.apply(
        lambda x: get_angle_from_two_points(
            x["x_lag_1"],
            x["y_lag_1"],
            x["x"],
            x["y"]
        ),
        axis=1,
    )

    tracking_df = tracking_df[df_columns]

    return tracking_df


def get_statsbomb_tracking_data(season: int):
    """ """
    tracking_df = pd.DataFrame()
    game_df = pd.DataFrame()

    try:
        os.mkdir("statsbomb")
    except Exception as e:
        logging.info(f"Unhandled exception: {e}")

    # try:
    #     os.mkdir(f"statsbomb/{season}")
    # except Exception as e:
    #     logging.info(f"Unhandled exception: {e}")

    sched_df = get_list_of_statsbomb_games()
    if season is not None:
        sched_df = sched_df[sched_df["season"] == season]
    tracking_urls_arr = sched_df["url"].to_numpy()

    for game in tracking_urls_arr:
        json_data = get_json_from_web_gz(game)
        game_id = json_data["nfl_game_id"]
        print(f"\nParsing {game_id}")
        game_df = parse_statsbomb_amf_tracking_data(json_data)

        game_df.to_csv(f"statsbomb/{game_id}.csv", index=False)
        game_df.to_parquet(f"statsbomb/{game_id}.parquet", index=False)
        del game_df
    return tracking_df


if __name__ == "__main__":
    print("starting up")
    for i in range(2018, 2024):
        get_statsbomb_tracking_data(i)

    # get_statsbomb_tracking_data(2019)
