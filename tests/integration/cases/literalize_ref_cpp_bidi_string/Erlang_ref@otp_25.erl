-module(fixture_literalize_ref_cpp_bidi_string_erlang_ref).
-export([x/0]).
x() ->
    Text = "a‪b",
    My_data = #{
        "value" => Text
    },
    My_data.
