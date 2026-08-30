#include <initializer_list>
#include <string>
#include <vector>
auto f(auto...) { return 0; }
int main() {
f(std::vector<std::vector<std::string>>{std::vector<std::string>{"DEL", "b", "10"}, std::vector<std::string>{"ADD", "a", "x"}});  // note
    return 0;
}
