#include <initializer_list>
#include <string>
#include <map>
int main() {
const auto* my_time = "01:02:03";
auto my_data = std::map<std::string, std::string>{
    {"x", my_time},
};
    (void)my_data;
    return 0;
}
