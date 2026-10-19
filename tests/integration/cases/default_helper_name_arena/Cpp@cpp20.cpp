#include <initializer_list>
#include <string>
#include <map>
int main() {
auto arena = std::map<std::string, int>{
    {"a", 1},
};
    (void)arena;
    return 0;
}
