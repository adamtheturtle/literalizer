#include <initializer_list>
#include <string>
#include <map>
template <typename... Args> auto process(Args...) { return 0; }
int main() {
process(std::map<std::string, LiteralizerVariant<int, std::string>>{{"a", 1}, {"b", "x"}});
    return 0;
}
