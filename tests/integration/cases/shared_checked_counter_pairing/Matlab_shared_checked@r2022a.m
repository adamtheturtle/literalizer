
function Fixture_shared_checked_counter_pairing_Matlab_shared_checked()
calls = 0;
checks = 0;
counter.accept = @accept;
checkResult(counter.accept("user_1", 100.0), {true, "first"})
checkResult(counter.accept("user_2", 101.0), {false, "second"})
assert(calls == 2 && checks == 2);
function actual = accept(user, timestamp)
    users = {"user_1", "user_2"};
    assert(strcmp(user, users{calls + 1}) && timestamp == 100.0 + calls);
    calls = calls + 1;
    actual = strcmp(user, "user_1");
end
function checkResult(actual, expected)
    reasons = {"first", "second"};
    assert(actual == expected{1} && strcmp(expected{2}, reasons{checks + 1}));
    checks = checks + 1;
end
end
