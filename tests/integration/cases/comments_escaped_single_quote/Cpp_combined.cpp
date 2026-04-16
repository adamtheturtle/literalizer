#include <initializer_list>
#include <string>
#include <map>
void check_() {
auto my_data = std::map<std::string, std::string>{
    {"key", "it's here"},  // a comment
};
my_data = std::map<std::string, std::string>{
    {"key", "it's here"},  // a comment
};
}
