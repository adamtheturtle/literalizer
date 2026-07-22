#include <initializer_list>
#include <string>
#include <map>
int main() {
auto my_data = std::map<std::string, std::nullptr_t>{};
    (void)my_data;
    return 0;
}
