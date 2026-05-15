-module(fixture_toml_table_dict_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "section" => #{"value" => 1}
    },
    My_data.
