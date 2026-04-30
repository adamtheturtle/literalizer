#include <initializer_list>
#include <string>
#include <map>
#include <vector>
auto process(auto...) { return 0; }
int main() {
auto my_var = 42;
process(std::map<std::string, int>{{"key", std::move(my_var)}, {"count", 42}});
    return 0;
}
