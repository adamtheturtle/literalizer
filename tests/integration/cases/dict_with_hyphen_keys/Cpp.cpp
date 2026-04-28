#include <initializer_list>
#include <string>
#include <map>
auto main() -> int {
auto my_data = std::map<std::string, std::string>{
    {"my-key", "value1"},
    {"another-key", "value2"},
    {"normal_key", "value3"},
};
    (void)my_data;
    return 0;
}
