#include <initializer_list>
#include <string>
#include <map>
#include <vector>
int main() {
auto val_x = std::map<std::string, std::string>{
    {"_", "_"},
};
auto val_y = std::map<std::string, std::string>{
    {"_", "_"},
};
auto my_data = std::make_tuple(
    std::move(val_x),
    std::move(val_y)
);
    (void)my_data;
    return 0;
}
