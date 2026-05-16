#include <initializer_list>
#include <string>
#include <map>
#include <vector>
#include <variant>
#include <tuple>
int main() {
auto my_data = std::vector<std::map<std::string, std::variant<std::string, std::tuple<int, std::string, std::string, int>>>>{
    std::map<std::string, std::variant<std::string, std::tuple<int, std::string, std::string, int>>>{{"call", "send"}, {"args", std::make_tuple(1, "email", "a@gmail.com", 100)}},
    std::map<std::string, std::variant<std::string, std::tuple<int, std::string, std::string, int>>>{{"call", "recv"}, {"args", std::make_tuple(2, "sms", "b@example.com", 200)}},
};
    (void)my_data;
    return 0;
}
