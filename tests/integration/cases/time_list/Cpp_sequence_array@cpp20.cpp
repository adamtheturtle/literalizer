#include <initializer_list>
#include <string>
#include <map>
#include <array>
#include <variant>
int main() {
auto my_data = std::map<std::string, std::array<std::string, 3>>{
    {"times", std::array<std::string, 3>{"09:30:00", "17:45:00", "23:59:59"}},
};
    (void)my_data;
    return 0;
}
