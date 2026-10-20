#include <initializer_list>
#include <string>
#include <map>
int main() {
auto key_binding = std::map<std::string, int>{
    {"a", 1},
};
    (void)key_binding;
    return 0;
}
