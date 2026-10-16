-module(fixture_cpp_mixed_sibling_maps_erlang).
-export([x/0]).
x() ->
    My_data = [
        [#{"a" => 1}, #{"a" => undefined}, 42],
        [#{"a" => 1}, #{"a" => "s"}, 42],
        [#{"a" => 1}, #{"a" => undefined}],
        [#{"a" => 1}, #{"a" => "s"}]
    ],
    My_data.
