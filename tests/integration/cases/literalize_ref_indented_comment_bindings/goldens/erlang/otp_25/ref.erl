-module(fixture_literalize_ref_indented_comment_bindings_erlang_ref).
-export([x/0]).
x() ->
            Shared = [
                1,
                2
            ],
            My_data = [
                % A leading comment with { braces, "quotes", and // markers
                "first\n{ \"quoted\" // text }",
                Shared
            ],
    My_data.
