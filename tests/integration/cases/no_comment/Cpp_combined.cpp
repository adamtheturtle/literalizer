#include <initializer_list>
#include <string>
#include <map>
void check_() {
auto my_data = std::map<std::string, std::string>{
    {"message", "no comment here"},
};
my_data = std::map<std::string, std::string>{
    {"message", "no comment here"},
};
}
