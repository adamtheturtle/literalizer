#include <initializer_list>
#include <string>
#include <map>
#include <variant>
int main() {
auto my_data = std::map<std::string, std::variant<std::string, int>>{
    {"host", "it's here"},  // a comment
    {"port", 80},  // another
};
    (void)my_data;
    return 0;
}
