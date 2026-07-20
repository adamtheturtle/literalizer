#include <initializer_list>
#include <string>
#include <map>
template <typename... Args> auto process(Args...) { return 0; }
int main() {
process(std::map<std::string, int>{{"a", 1}, {"b", 2}});
    return 0;
}
