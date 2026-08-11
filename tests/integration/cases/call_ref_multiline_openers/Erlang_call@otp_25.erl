-module(fixture_call_ref_multiline_openers_erlang_call).
-export([x/0]).
consume(_, _) -> ok.
x() ->
    Foo = 42,
    consume([
        #{
            "other" => 1
        },
        Foo
    ], #{
        "left" => Foo,
        "other" => 1
    }).
