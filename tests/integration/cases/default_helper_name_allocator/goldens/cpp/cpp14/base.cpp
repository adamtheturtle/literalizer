#include <map>
#include <string>
int main() {
auto allocator = std::map<std::string, int>{
    {"a", 1},
};
    (void)allocator;
    return 0;
}
