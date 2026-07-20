#include <initializer_list>
#include <string>
#include <map>
#include <variant>
int main() {
auto my_data = std::map<std::string, std::string>{
    {"date", "2024-01-15"},
    {"datetime", "2024-01-15T12:30:00+00:00"},
};
    (void)my_data;
    return 0;
}
