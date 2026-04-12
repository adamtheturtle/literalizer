import std.json;
void _check() {
print(throttler.check("user_1", 1000.0))
print(throttler.check("user_2", 2000.5))
}
