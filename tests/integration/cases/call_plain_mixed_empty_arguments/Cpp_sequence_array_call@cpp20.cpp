#include <array>
#include <cstddef>
#include <string>
auto make_widget(auto...) { return 0; }
int main() {
static_cast<void>(make_widget(std::array<std::nullptr_t, 0>{}, std::array<int, 1>{1}, std::array<std::nullptr_t, 0>{}));
static_cast<void>(make_widget(std::array<std::string, 1>{"text"}, std::array<int, 1>{2}, std::array<std::nullptr_t, 0>{}));
static_cast<void>(make_widget(std::array<std::nullptr_t, 0>{}, std::array<std::string, 1>{"text"}, std::array<std::nullptr_t, 0>{}));
static_cast<void>(make_widget(std::array<std::string, 1>{"text"}, std::array<int, 1>{2}, std::array<int, 1>{3}));
    return 0;
}
