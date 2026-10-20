#include <initializer_list>
#include <string>
#include <vector>
#include <cstddef>
#include <variant>
struct thingType_ { template <typename... Args> [[nodiscard]] auto go(Args...) const { return 0; } };
const thingType_ thing;
int main() {
static_cast<void>(thing.go(std::vector<std::nullptr_t>{}, std::vector<int>{1}, std::vector<std::nullptr_t>{}));
static_cast<void>(thing.go(std::vector<std::string>{"text"}, std::vector<int>{2}, std::vector<std::nullptr_t>{}));
static_cast<void>(thing.go(std::vector<std::nullptr_t>{}, std::vector<std::string>{"text"}, std::vector<std::nullptr_t>{}));
static_cast<void>(thing.go(std::vector<std::string>{"text"}, std::vector<int>{2}, std::vector<int>{3}));
    return 0;
}
