#include <array>
#include <cstddef>
#include <string>
struct thingType_ { template <typename... Args> [[nodiscard]] auto go(Args...) const { return 0; } };
const thingType_ thing;
int main() {
static_cast<void>(thing.go(std::array<std::nullptr_t, 0>{}, std::array<int, 1>{1}, std::array<std::nullptr_t, 0>{}));
static_cast<void>(thing.go(std::array<std::string, 1>{"text"}, std::array<int, 1>{2}, std::array<std::nullptr_t, 0>{}));
static_cast<void>(thing.go(std::array<std::nullptr_t, 0>{}, std::array<std::string, 1>{"text"}, std::array<std::nullptr_t, 0>{}));
static_cast<void>(thing.go(std::array<std::string, 1>{"text"}, std::array<int, 1>{2}, std::array<int, 1>{3}));
    return 0;
}
