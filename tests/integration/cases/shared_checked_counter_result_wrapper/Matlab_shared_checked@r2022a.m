
function Fixture_shared_checked_counter_result_wrapper_Matlab_shared_checked()
calls = 0;
checks = 0;
counter.accept = @accept;
checkResult(counter.accept("user_1", 100.0), {true, "first"})
assert(calls == 1 && checks == 1);
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
