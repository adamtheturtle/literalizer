#include <initializer_list>
#include <string>
#include <map>
#include <vector>
struct NamedType { int id{}; std::string description; bool is_done{}; std::vector<int> blocks; };
int main() {
auto my_data = std::vector<NamedType>{
    NamedType{100, "first task", false, std::vector<int>{102, 103}},
    NamedType{101, "second task", true, std::vector<int>{100}},
};
    (void)my_data;
    return 0;
}
