from parse_statsbomb_data import get_json_from_web_gz,get_list_of_statsbomb_games

def check_data_advalibility():
    games_df = get_list_of_statsbomb_games()
    game_ids_arr = games_df["nfl_game_id"].to_numpy()

if __name__ =="__main__":
    url = "https://github.com/sportsdataverse/amf-location-data/releases/download/amf_tracking_parquet/2022_03_GB_TB.parquet"
    json_data = get_json_from_web_gz(url)