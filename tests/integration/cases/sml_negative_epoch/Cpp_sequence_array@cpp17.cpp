#include <initializer_list>
#include <string>
#include <array>
int main() {
auto my_data = std::array<std::string, 1>{
    "1960-01-01T00:00:00+00:00",
};
    (void)my_data;
    return 0;
}
