#include <initializer_list>
#include <string>
#include <map>
int main() {
auto my_data = std::map<std::string, std::string>{
    // heading
    {"a", "single ' // data"},
    {"b", "linecontinuation"},
    {"c", "\\"},  // actual comment
    {"d", "  "},  // final comment
};
(void)my_data;
my_data = std::map<std::string, std::string>{
    // heading
    {"a", "single ' // data"},
    {"b", "linecontinuation"},
    {"c", "\\"},  // actual comment
    {"d", "  "},  // final comment
};
    (void)my_data;
    return 0;
}
