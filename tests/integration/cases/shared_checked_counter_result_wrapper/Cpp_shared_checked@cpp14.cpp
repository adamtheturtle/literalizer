#include <tuple>
#include <cassert>
#include <string>
class Counter {
    int calls_ = 0;
public:
#if __cplusplus >= 201703L
    [[nodiscard]]
#endif
    int count() const noexcept { return calls_; }
    bool accept(const std::string& user, double timestamp) {
        assert(user == (calls_ == 0 ? "user_1" : "user_2"));
        assert(timestamp == 100.0 + calls_);
        ++calls_;
        return user == "user_1";
    }
};
int main() try {
    Counter counter;
    int checks = 0;
    const auto checkResult = [&checks](bool actual, const std::tuple<bool, std::string>& expected) {
        assert(actual == std::get<0>(expected));
        assert(std::get<1>(expected) == (checks == 0 ? "first" : "second"));
        ++checks;
    };
    checkResult(counter.accept("user_1", 100.0), std::make_tuple(true, "first"));
    assert(counter.count() == 1 && checks == 1);
    return 0;
} catch (...) {
    return 1;
}
