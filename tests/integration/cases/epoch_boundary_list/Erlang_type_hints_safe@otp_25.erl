-module(fixture_epoch_boundary_list_erlang_type_hints_safe).
-export([x/0]).
x() ->
    My_data = [
        "1901-12-13T20:45:51",
        "1901-12-13T20:45:52",
        "2038-01-19T03:14:07",
        "2038-01-19T03:14:08"
    ],
    My_data.
