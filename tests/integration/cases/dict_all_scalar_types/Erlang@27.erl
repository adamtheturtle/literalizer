-module(fixture_dict_all_scalar_types_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "s" => "string",
        "i" => 1,
        "f" => 1.5,
        "b" => true,
        "n" => undefined,
        "d" => "2024-01-15",
        "dt" => "2024-01-15T12:00:00",
        "by" => <<72, 101, 108, 108, 111>>
    },
    My_data.
