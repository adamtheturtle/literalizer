-module(fixture_epoch_boundary_set_erlang_type_hints_safe).
-export([x/0]).
x() ->
    My_data = sets:from_list([
        "1901-12-13T20:45:51",
        "1901-12-13T20:45:52",
        "2038-01-19T03:14:07",
        "2038-01-19T03:14:08"
    ]),
    My_data.
