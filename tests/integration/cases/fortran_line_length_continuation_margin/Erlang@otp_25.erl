-module(fixture_fortran_line_length_continuation_margin_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "deep" => [[[[[[1]]]]]]
    },
    My_data.
