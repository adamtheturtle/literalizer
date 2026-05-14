#include <initializer_list>
#include <string>
#include <map>
#include <vector>
#include <variant>
int main() {
auto my_data = std::map<std::string, std::vector<std::nullptr_t>>{
    {"times", std::vector<std::nullptr_t>{"09:30:00", "17:45:00", "23:59:59"}},
};
    (void)my_data;
    return 0;
}
