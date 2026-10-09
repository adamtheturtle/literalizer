#include <initializer_list>
#include <string>
#include <map>
int main() {
static auto my_data = std::map<std::string, int>{
    // Field declaration
    {"one", 1},
    {"two", 2},
};
(void)my_data;
my_data = std::map<std::string, int>{
    // Field declaration
    {"one", 1},
    {"two", 2},
};
    (void)my_data;
    return 0;
}
