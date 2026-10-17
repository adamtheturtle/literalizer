#include <initializer_list>
#include <string>
#include <map>
int main() {
const auto* value = "12:30:15+02:00";
auto my_data = std::map<std::string, std::string>{
    {"x", value},
};
    (void)my_data;
    return 0;
}
