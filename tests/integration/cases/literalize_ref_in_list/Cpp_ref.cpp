#include <initializer_list>
#include <string>
#include <map>
#include <vector>
int main() {
const auto val_x = std::map<std::string, std::string>{
    {"_", "_"},
};
const auto val_y = std::map<std::string, std::string>{
    {"_", "_"},
};
const auto my_data = std::vector<std::map<std::string, std::string>>{
    val_x,
    val_y,
};
    (void)my_data;
    return 0;
}
