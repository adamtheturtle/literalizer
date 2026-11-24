import std.json;
struct Counter {
    int calls;
    bool accept(string user, double timestamp) {
        assert(user == (calls == 0 ? "user_1" : "user_2"));
        assert(timestamp == 100.0 + calls);
        calls++;
        return user == "user_1";
    }
}
int checks;
void checkResult(bool actual, JSONValue expected) {
    assert(actual == expected.array[0].boolean);
    assert(expected.array[1].str == (checks == 0 ? "first" : "second"));
    checks++;
}
void main() {
    Counter counter;
    checkResult(counter.accept("user_1", 100.0), JSONValue([JSONValue(true), JSONValue("first")]));
    assert(counter.calls == 1 && checks == 1);
}
