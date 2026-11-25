-module(fixture_string_with_dollar_brace_erlang_sequence_tuple).
-export([x/0]).
x() ->
    My_data = {
        "prefix ${HOME} suffix",
        "${interpolated}"
    },
    My_data.
