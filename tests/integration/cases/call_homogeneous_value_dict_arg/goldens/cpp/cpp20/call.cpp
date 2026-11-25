#include <map>
#include <string>
auto process(auto...) { return 0; }
int main() {
process(std::map<std::string, int>{{"a", 1}, {"b", 2}});
    return 0;
}
