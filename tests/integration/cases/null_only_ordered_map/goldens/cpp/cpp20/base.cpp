#include <cstddef>
#include <string>
#include <utility>
#include <vector>
int main() {
auto my_data = std::vector<std::pair<std::string, std::nullptr_t>>{
    {"missing", nullptr},
};
    (void)my_data;
    return 0;
}
