-module(fixture_datetime_epoch_wide_set_erlang_type_hints_safe).
-export([x/0]).
x() ->
    My_data = sets:from_list([
        "2099-06-15T08:30:00"
    ]),
    My_data.
