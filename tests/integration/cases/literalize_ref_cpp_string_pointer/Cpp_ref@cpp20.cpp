#include <initializer_list>
#include <string>
#include <map>
int main() {
const auto* shared = "s";
auto my_data = std::map<std::string, std::string>{
    {"value", shared},
};
    (void)my_data;
    return 0;
}
