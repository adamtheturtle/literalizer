#include "../../cpp_support/include/named_type.hpp"
#include <initializer_list>
#include <string>
#include <map>
#include <vector>
int main() {
auto my_data = std::vector<NamedType>{
    NamedType{100, "first entry", false, std::vector<int>{102, 103}},
    NamedType{101, "second entry", true, std::vector<int>{100}},
};
    (void)my_data;
    return 0;
}
