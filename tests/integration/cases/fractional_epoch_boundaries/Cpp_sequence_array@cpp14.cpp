#include <initializer_list>
#include <string>
#include <array>
int main() {
auto my_data = std::array<std::string, 3>{
    "1970-01-01T00:00:00.000001+00:00",
    "1969-12-31T23:59:59.500000+00:00",
    "1970-01-01T00:00:01+00:00",
};
    (void)my_data;
    return 0;
}
