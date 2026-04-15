#include <initializer_list>
#include <string>
#include <map>
void check_() {
auto my_data = std::map<std::string, std::string>{
    {"my-key", "value1"},
    {"another-key", "value2"},
    {"normal_key", "value3"},
};
}
