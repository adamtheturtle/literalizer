#include <initializer_list>
#include <string>
#include <array>
int main() {
auto my_data = std::array<std::string, 4>{
    "1901-12-13T20:45:51",
    "1901-12-13T20:45:52",
    "2038-01-19T03:14:07",
    "2038-01-19T03:14:08",
};
    (void)my_data;
    return 0;
}
