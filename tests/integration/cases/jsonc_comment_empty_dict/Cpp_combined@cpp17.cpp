#include <initializer_list>
#include <string>
#include <map>
#include <cstddef>
int main() {
// empty heading
// empty body
// after empty
auto my_data = std::map<std::string, std::nullptr_t>{};
(void)my_data;
// empty heading
// empty body
// after empty
my_data = std::map<std::string, std::nullptr_t>{};
    (void)my_data;
    return 0;
}
