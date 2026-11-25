#include <cstddef>
#include <map>
#include <string>
int main() {
auto my_data = std::map<std::string, std::nullptr_t>{
    {"a", nullptr},
    {"b", nullptr},
    // trailing
};
(void)my_data;
my_data = std::map<std::string, std::nullptr_t>{
    {"a", nullptr},
    {"b", nullptr},
    // trailing
};
    (void)my_data;
    return 0;
}
