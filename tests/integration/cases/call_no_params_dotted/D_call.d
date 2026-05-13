import std.json;
void main() {
struct ThrottlerType_ { int check(T...)(T args) { return 0; } }
ThrottlerType_ throttler;
throttler.check();
throttler.check();
}
