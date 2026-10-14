-module(fixture_rust_epoch_boundary_set_erlang_datetime_epoch).
-export([x/0]).
x() ->
    My_data = sets:from_list([
        -2147483649,
        -2147483648,
        2147483647,
        2147483648
    ]),
    My_data.
