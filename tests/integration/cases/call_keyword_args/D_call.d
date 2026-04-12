import std.json;
struct _throttlerType { auto check(T...)(T args) { return 0; } }
_throttlerType throttler;
auto print(T...)(T args) { return 0; }
void _check() {
print(throttler.check("user_1", 1000.0))
print(throttler.check("user_2", 2000.5))
}
