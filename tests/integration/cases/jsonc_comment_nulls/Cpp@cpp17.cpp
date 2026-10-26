#include <cstddef>
#include <map>
#include <string>
int main() {
auto my_data = std::map<std::string, std::nullptr_t>{
    // null heading
    // before null
    {"a", nullptr},  // first null
    {"b", nullptr},  // second null
};
    (void)my_data;
    return 0;
}
