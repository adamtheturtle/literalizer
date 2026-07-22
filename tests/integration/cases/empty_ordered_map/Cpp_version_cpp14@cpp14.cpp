#include <initializer_list>
#include <string>
#include <utility>
#include <vector>
int main() {
auto my_data = std::vector<std::pair<std::string, std::nullptr_t>>{};
    (void)my_data;
    return 0;
}
