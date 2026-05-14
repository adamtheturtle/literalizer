local throttler = { check(user_id, ts):: null };
local emit(_arg) = null;
[
    emit(throttler.check(user_id="user_1", ts=1000.0)),
    emit(throttler.check(user_id="user_2", ts=2000.5)),
]
