class ThrottlerType; def check(*a); end; end
throttler = ThrottlerType.new
def print(*a); end
print(throttler.check(user_id: "user_1", ts: 1000.0))
print(throttler.check(user_id: "user_2", ts: 2000.5))
