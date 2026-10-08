-module(fixture_literalize_ref_jsonc_comments_erlang_ref).
-export([x/0]).
x() ->
    Existing = #{
        "_" => "_"
    },
    My_data = Existing,
    My_data.
