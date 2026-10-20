#include <initializer_list>
#include <string>
#include <map>
int main() {
auto allocator = std::map<std::string, int>{
    {"a", 1},
};
    (void)allocator;
    return 0;
}
