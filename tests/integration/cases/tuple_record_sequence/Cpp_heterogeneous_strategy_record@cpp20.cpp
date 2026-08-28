#include <initializer_list>
#include <string>
#include <vector>
#include <variant>
struct Record0 { std::string call; std::vector<std::variant<int, std::string>> args; };
int main() {
auto my_data = std::vector{
    Record0{.call = "send", .args = {1, "email", "a@gmail.com", 100}},
    Record0{.call = "recv", .args = {2, "sms", "b@example.com", 200}},
};
    (void)my_data;
    return 0;
}
