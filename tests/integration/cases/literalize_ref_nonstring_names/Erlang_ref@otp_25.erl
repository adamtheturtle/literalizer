-module(fixture_literalize_ref_nonstring_names_erlang_ref).
-export([x/0]).
x() ->
    Actual = #{
        "_" => "_"
    },
    My_data = [
        #{"$ref" => 1},
        #{"$ref" => undefined},
        Actual
    ],
    My_data.
