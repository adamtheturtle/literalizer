#include <map>
#include <string>
template <typename... Args> auto consume(Args...) { return 0; }
int main() {
auto item = 42;
consume(std::map<std::string, int>{{"field", item}});
    return 0;
}
