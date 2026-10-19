#include <initializer_list>
#include <string>
#include <map>
int main() {
auto k = std::map<std::string, int>{
    {"a", 1},
};
    (void)k;
    return 0;
}
