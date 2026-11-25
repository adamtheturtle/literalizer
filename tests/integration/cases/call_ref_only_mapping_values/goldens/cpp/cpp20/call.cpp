#include <map>
#include <string>
auto consume(auto...) { return 0; }
int main() {
auto item = 42;
consume(std::map<std::string, int>{{"field", item}});
    return 0;
}
