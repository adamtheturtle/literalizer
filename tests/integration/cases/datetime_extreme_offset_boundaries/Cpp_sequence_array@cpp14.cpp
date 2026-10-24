#include <initializer_list>
#include <string>
#include <array>
int main() {
auto my_data = std::array<std::string, 4>{
    "2020-06-15T12:00:00-23:59",
    "2020-06-15T12:00:00-18:00",
    "2020-06-15T12:00:00+18:00",
    "2020-06-15T12:00:00+23:59",
};
    (void)my_data;
    return 0;
}
