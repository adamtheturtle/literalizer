#include <initializer_list>
#include <string>
#include <map>
int main() {
const auto my_var = std::map<std::string, std::string>{
    {"_", "_"},
};
const auto my_data = std::map<std::string, std::map<std::string, std::string>>{
    {"key", my_var},
};
    (void)my_data;
    return 0;
}
