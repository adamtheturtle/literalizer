-module(fixture_literalize_ref_pre_indented_injected_text_erlang_ref).
-export([x/0]).
x() ->
                Shared = [
                    1,
                    2
                ],
                Other = 3,
                Payload = "\n    shared : Val\nshared = RInt 99",
                My_data = #{
                    "a" => Shared,
                    "b" => Other,
                    "payload" => Payload
                },
    My_data.
