-module(fixture_literalize_ref_deep_nesting_erlang_ref).
-export([x/0]).
x() ->
    Deep = [
        [
            1,
            2
        ],
        [
            3,
            4
        ]
    ],
    My_data = #{
        "a" => #{
            "b" => #{
                "c" => Deep
            }
        }
    },
    My_data.
