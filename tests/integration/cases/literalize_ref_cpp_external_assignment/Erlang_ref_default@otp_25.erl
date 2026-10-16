-module(fixture_literalize_ref_cpp_external_assignment_erlang_ref_default).
-export([x/0]).
x() ->
    Ref_data = [
        1,
        2
    ],
    My_data = [
        0
    ],
    (void)my_data;
    My_data = Ref_data,
    (void)my_data;.
