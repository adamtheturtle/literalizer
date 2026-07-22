#include <initializer_list>
#include <string>
#include <map>
#include <vector>
int main() {
auto ref_x = std::map<std::string, std::string>{
    {"_", "_"},
};
auto my_data = std::make_tuple(
    std::move(ref_x),
    1,
    2
);
    (void)my_data;
    return 0;
}
