#include <cstddef>
#include <string>
#include <vector>
template <typename... Args> auto make_widget(Args...) { return 0; }
int main() {
static_cast<void>(make_widget(std::vector<std::nullptr_t>{}, std::vector<int>{1}, std::vector<std::nullptr_t>{}));
static_cast<void>(make_widget(std::vector<std::string>{"text"}, std::vector<int>{2}, std::vector<std::nullptr_t>{}));
static_cast<void>(make_widget(std::vector<std::nullptr_t>{}, std::vector<std::string>{"text"}, std::vector<std::nullptr_t>{}));
static_cast<void>(make_widget(std::vector<std::string>{"text"}, std::vector<int>{2}, std::vector<int>{3}));
    return 0;
}
