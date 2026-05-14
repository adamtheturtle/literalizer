import std.json;
void main() {
struct ThrottlerType_ { int check(T...)(T args) { return 0; } }
ThrottlerType_ throttler;
int emit(T...)(T args) { return 0; }
emit(throttler.check("user_1", 1000.0));
emit(throttler.check("user_2", 2000.5));
}
