import std.json;
void _check() {
struct ThrottlerType_ { int check(T...)(T args) { return 0; } }
ThrottlerType_ throttler;
int print(T...)(T args) { return 0; }
print(throttler.check("user_1", 1000.0));
print(throttler.check("user_2", 2000.5));
}
