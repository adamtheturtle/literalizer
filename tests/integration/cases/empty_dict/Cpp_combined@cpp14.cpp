#include <initializer_list>
#include <string>
#include <map>
#include <cstddef>
int main() {
auto my_data = std::map<std::string, std::nullptr_t>{};
(void)my_data;
my_data = std::map<std::string, std::nullptr_t>{};
    (void)my_data;
    return 0;
}
