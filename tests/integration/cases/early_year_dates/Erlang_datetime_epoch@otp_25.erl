-module(fixture_early_year_dates_erlang_datetime_epoch).
-export([x/0]).
x() ->
    My_data = #{
        "date" => "0099-05-27",
        "naive" => -62135551800,
        "recent" => 1716804000
    },
    My_data.
