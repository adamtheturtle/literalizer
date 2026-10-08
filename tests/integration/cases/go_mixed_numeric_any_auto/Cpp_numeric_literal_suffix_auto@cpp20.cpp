#include <initializer_list>
#include <string>
#include <map>
#include <variant>
int main() {
auto my_data = std::map<std::string, std::variant<double, long, std::string>>{
    {"f", 1.5},
    {"n", -3L},
    {"s", "x"},
};
    (void)my_data;
    return 0;
}
