#include <initializer_list>
#include <string>
#include <map>
#include <vector>
#include <variant>
int main() {
auto my_data = std::vector<std::map<std::string, std::variant<std::string, std::vector<std::variant<int, std::string>>>>>{
    std::map<std::string, std::variant<std::string, std::vector<std::variant<int, std::string>>>>{{"call", "send"}, {"args", std::vector<std::variant<int, std::string>>{1, "email", "a@gmail.com", 100}}},
    std::map<std::string, std::variant<std::string, std::vector<std::variant<int, std::string>>>>{{"call", "recv"}, {"args", std::vector<std::variant<int, std::string>>{2, "sms", "b@example.com", 200}}},
};
(void)my_data;
my_data = std::vector<std::map<std::string, std::variant<std::string, std::vector<std::variant<int, std::string>>>>>{
    std::map<std::string, std::variant<std::string, std::vector<std::variant<int, std::string>>>>{{"call", "send"}, {"args", std::vector<std::variant<int, std::string>>{1, "email", "a@gmail.com", 100}}},
    std::map<std::string, std::variant<std::string, std::vector<std::variant<int, std::string>>>>{{"call", "recv"}, {"args", std::vector<std::variant<int, std::string>>{2, "sms", "b@example.com", 200}}},
};
    (void)my_data;
    return 0;
}
