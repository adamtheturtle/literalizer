-module(fixture_date_key_dict_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "2024-01-01" => "new_year",
        "2024-07-04" => "independence_day",
        "2024-12-25" => "christmas"
    },
    My_data.
