#include <initializer_list>
#include <string>
#include <map>
#include <array>
#include <cstddef>
int main() {
auto my_data = {
    std::map<std::string, std::string>{{"timestamp", "2020-01-01T00:00:00+00:00"}},
    std::map<std::string, std::string>{},
};
    (void)my_data;
    return 0;
}
