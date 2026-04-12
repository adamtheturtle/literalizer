-module(check).
-export([x/0]).
x() ->
    print(throttler.check("user_1", 1000.0))
    print(throttler.check("user_2", 2000.5)),
    My_data.
