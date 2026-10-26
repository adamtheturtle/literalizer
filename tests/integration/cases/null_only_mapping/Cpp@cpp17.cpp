#include <cstddef>
#include <map>
#include <string>
int main() {
auto my_data = std::map<std::string, std::nullptr_t>{
    {"value", nullptr},
};
    (void)my_data;
    return 0;
}
