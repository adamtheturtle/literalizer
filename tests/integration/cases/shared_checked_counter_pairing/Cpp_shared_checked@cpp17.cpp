#include <tuple>
#include <cassert>
#include <string>
#include <tuple>
struct Counter {
    int calls = 0;
    bool accept(const std::string& user, double timestamp) {
        assert(user == (calls == 0 ? "user_1" : "user_2"));
        assert(timestamp == 100.0 + calls);
        ++calls;
        return user == "user_1";
    }
};
static int checks = 0;
static void checkResult(bool actual, const std::tuple<bool, std::string>& expected) {
    assert(actual == std::get<0>(expected));
    assert(std::get<1>(expected) == (checks == 0 ? "first" : "second"));
    ++checks;
}
int main() {
    Counter counter;
    checkResult(counter.accept("user_1", 100.0), std::make_tuple(true, "first"));
    checkResult(counter.accept("user_2", 101.0), std::make_tuple(false, "second"));
    assert(counter.calls == 2 && checks == 2);
}
