
calls = Ref(0)
checks = Ref(0)
counter = (accept = function(user, timestamp)
    @assert user == (calls[] == 0 ? "user_1" : "user_2")
    @assert timestamp == 100.0 + calls[]
    calls[] += 1
    user == "user_1"
end,)
function checkResult(actual, expected)
    @assert actual == expected[1]
    @assert expected[2] == (checks[] == 0 ? "first" : "second")
    checks[] += 1
end
checkResult(counter.accept("user_1", 100.0), [true, "first"])
@assert calls[] == 1 && checks[] == 1
