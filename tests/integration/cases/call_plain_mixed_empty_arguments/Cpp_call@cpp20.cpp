#include <initializer_list>
#include <string>
#include <vector>
#include <cstddef>
#include <variant>
auto make_widget(auto...) { return 0; }
int main() {
static_cast<void>(make_widget(std::vector<std::nullptr_t>{}, std::vector<int>{1}, std::vector<std::nullptr_t>{}));
static_cast<void>(make_widget(std::vector<std::string>{"text"}, std::vector<int>{2}, std::vector<std::nullptr_t>{}));
static_cast<void>(make_widget(std::vector<std::nullptr_t>{}, std::vector<std::string>{"text"}, std::vector<std::nullptr_t>{}));
static_cast<void>(make_widget(std::vector<std::string>{"text"}, std::vector<int>{2}, std::vector<int>{3}));
    return 0;
}
