
local calls, checks = 0, 0
local counter = {}
counter.accept = function(user, timestamp)
    assert(user == (calls == 0 and "user_1" or "user_2"))
    assert(timestamp == 100.0 + calls)
    calls = calls + 1
    return user == "user_1"
end
local function checkResult(actual, expected)
    assert(actual == expected[1])
    assert(expected[2] == (checks == 0 and "first" or "second"))
    checks = checks + 1
end
checkResult(counter.accept("user_1", 100.0), {true, "first"})
checkResult(counter.accept("user_2", 101.0), {false, "second"})
assert(calls == 2 and checks == 2)
