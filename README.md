# amf-location-data <img alt="StatsBombPython_Lock" src="https://github.com/sportsdataverse/amf-location-data/blob/main/statsbomb_color_positive_logo.jpg" align="right" height="40"/>

This is a data repository that parses StatsBomb's high-frequency tracking data found in the [`statsbomb/amf-open-data`](https://github.com/statsbomb/amf-open-data) GitHub repository into a table format similar to datasets seen in the NFL Big Data Bowl (BDB).

## Datasets

If you want to view the resulting `.csv` files, go to the [Tracking Data - CSV](https://github.com/sportsdataverse/amf-location-data/releases/tag/amf_tracking_csv) release to view all games currently parsed as a `.csv` file.

If you want to view the resulting `.parquet` files, go to the [Tracking Data - Parquet](https://github.com/sportsdataverse/amf-location-data/releases/tag/amf_tracking_parquet) release to view all games currently parsed as a `.parquet` file.

> **Note**: The resulting `.parquet` files are significantly smaller than an equivalent `.csv` file. If you can, download a game's `.parquet` file instead of that game's `.csv` file.

## Column Names

Most columns follow the naming/data conventions present in the StatsBomb's full tracking dictionary, which can be accessed (through this link)[https://github.com/statsbomb/amf-open-data/blob/main/doc/full_tracking_dictionary.pdf].

Here is a full list of columns that can be found in either a `.csv` or `.parquet` file from this GitHub repository. Each row is a player's location in a specific frame.

| c_name   | c_datatype | c_description   | c_example   |
| -- | -- | -- | -- |
| season   | int   | The NFL season this play/frame occured in.   | `2020`   |
| season_id   | int   | Statsbomb's unique identifier for the season this play is from.   | `90`   |
| season_name   | str   | Statsbomb's name for this specific season.   | `"2020/2021"`   |
| game_id   | int   | Statsbomb's unique identifier for the game this play is from.   | `1503728`   |
| nfl_game_id   | str   | The NFL GSIS unique identifier for the game this play is occuring in.   | `"2020_04_LAC_TB"`   |
| nfl_old_game_id   | int   | An older game ID system used by NFL GSIS. Only here for compatibility reasons, and if you can, use `[nfl_game_id]` instead.   | `2020100407`   |
| competition_id   | int   | Statsbomb's unique identifier for the league this play is from.   | `1409`   |
| competition_name   | str   | The name of the leauge this play is from.   | `"NFL"`, `"NCAA"`   |
| game_date   | date   | The date of the game.   | `"2020-09-20"`   |
| play_quarter   | int   | The quarter this play occurred in.   | `1`, `2`, `3`,`4`   |
| team_id   | int   | Statsbomb's unique identifier for the league this play is from.   | `1000947`   |
| nfl_team_id   | str   | The team ID (abbreviation) of the team the player being focused on in this frame.   | `"TB"`, `"LAC"`   |
| play_uuid   | uuid   | Statsbomb's unique identifier for this specific play.   | `5f93de4d-126a-43cc-8edc-a3119eaff859` |
| gsis_play_id   | int   | NFL GSIS' identifier for this play. This is not a unique identifer. Multiple games can have the exact same `[gsis_play_id]`.   | `56`   |
| play_yardline   | int   | The line of scrimage for this play. Where `25` means that it is on the offensive team's 25 yard line, while `95` means that the offense only needs to travel 5 additional yards to score a touchdown.   | `25`, `95`   |
| offense_left_to_right   | bool   | Boolean flag indicating if the offense is traveling from left to right (A.K.A.: offense needs to travel in a positive X direction to gain a first down/score a touchdown), or right to left (A.K.A.: offense needs to travel in a negative X direction to gain a first down/score a touchdown.) | `TRUE`, `FALSE`   |
| play_direction   | str   | Similar to `[offense_left_to_right]`. Intended to mirror the `[playDirection]` column found in NFL Big Data Bowl (BDB) tracking datasets.   | `"left"`, `"right"`   |
| game_clock   | int   | The number of seconds left in the quarter at the time the ball is snapped for this play   | `900`, `820`   |
| player_id   | int   | Statsbomb's unique identifier for the player being focused on in this frame.   | `1003205`   |
| gsis_player_id   | int   | The NFL GSIS unique identifier for the player being focused on in this play.   | `35481`   |
| position_code   | str   | The abbreviation of the position for this player being focused on in this frame.   | `"TE"`   |
| player_jersey_number   | int   | The jersey number for the player being focused on in this frame.   | `87`   |
| player_name   | str   | The name of the player being focused on in this frame.   | `"Rob Gronkowski"`   |
| on_camera_ratio   | decimal   | The ratio on how often this player is visible in the play on camera. An `[on_camera_ratio]` of `0.88` means that the player was visible on camera for 88% of all frames for this play.   | `0.88`   |
| player_coverage_count   | int   | The number of players covered by Statsbomb in this play.   | `18`, `22`   |
| calibration_fault_ratio | decimal   | The proportion of frames with potential issues with calibration   | `0`, `0.5`   |
| track_id   | uuid   | Statsbomb's unique identifier for this specific frame.   | `6e308f9e-b049-45fd-b8d0-bc656d0eceb3` |
| frame_num   | int   | The numbered frame this row is for this player for this play. This starts at `0`, and incriments by one for every frame.   | `0`, `1`, ..., `379`   |
| timestamp   | int   | The timestamp (in milliseconds), from the video this tracking data was sourced from, that this frame occurs at.   | `56933333`   |
| tracking_framerate   | int   | The framerate for the tracking data. 30 means that the tracking data is running at 30 frames per second. For comparison, the tracking data seen in NFL BDB competitions run at 10 frames per second.   | `30`   |
| time_since_last_frame   | float   | The time (in seconds) that has elapsed since the previous frame.   | `0.033`  |
| play_start_timestamp   | int   | The timestamp (in milliseconds), from the video this tracking data was sourced from, of when the tracking data for this play starts at.   | `44330675`   |
| play_end_timestamp   | int   | The timestamp (in milliseconds), from the video this tracking data was sourced from, of when the tracking data for this play ends at.   | `59005108`   |
| player_start_timestamp  | int   | The timestamp (in milliseconds), from the video this tracking data was sourced from, of when the tracking data for this play starts at, for this player.   | `44300000`   |
| player_end_timestamp   | int   | The timestamp (in milliseconds), from the video this tracking data was sourced from, of when the tracking data for this play ends at, for this player.   | `57200000`   |
| time_since_snap   | decimal   | The number of seconds before or after the ball is snapped, and the actual play starts. If `[time_since_snap]` is negative, this frame occurs before the ball is snapped, and if `[time_since_snap]` is positive, the ball has already been snaped for this play.   | `-8.147`, `-1.081`, `1.186`, `3.053` |
| x   | decimal   | The static X coordinate for this player in this frame. This is similar to the `[x]` column seen in NFL BDB tracking datasets. This should be a number between `0` and `120`.   | `19.51`   |
| y   | decimal   | The static Y coordinate for this player in this frame. This is similar to the `[y]` column seen in NFL BDB tracking datasets. This should be a number between `0` and `53.3`.   | `33.89`   |
| ngs_x   | decimal   | A transformed NFL Next Gen Stats (NGS) x coordinate for this player in this frame.   | `207.06`   |
| ngs_y   | decimal   | A transformed NFL Next Gen Stats (NGS) y coordinate for this player in this frame.   | `233.34`   |
| player_speed   | float   | The speed of this player in this frame, in yards per second (yds/s). This is calculated by taking the location of this player in frame `n`, determining the distance between frame `n` and frame `n-5`, and the time elapsed between frame `n` and frame `n-5`.   | `2.839106489`, `3.091235808`   |
| player_acceleration   | float   | The acceleration of this player in this frame, in yards per second (yds/s^2).   | `-1.04862012`, `1.483138115`   |
| player_distance   | float   | The distance traveled by this player (in yards) from frame `n-1` to frame `n`.   | `0.098488578`   |
| player_orientation   | float   | The orientation of the player, in degrees, where 0° is facing positive Y.   | `338.4046896`   |
| player_direction   | float   | The direction the player is traveling, in degrees, where 0° is facing positive Y.   | `336.037511`   |

## Other Notes

The usage of this data is still bound by the [StatsBomb Public Data User Agreement](https://github.com/statsbomb/amf-open-data/blob/main/LICENSE.pdf). Please ensure that the usage of data from this and the [`statsbomb/amf-open-data`](https://github.com/statsbomb/amf-open-data) GitHub repositories follows this User Agreement.
