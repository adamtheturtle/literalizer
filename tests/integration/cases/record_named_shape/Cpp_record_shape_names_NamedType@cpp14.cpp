#include "../../cpp_support/include/named_type.hpp"
#include <vector>
int main() {
auto my_data = std::vector<NamedType>{
    NamedType{100, "first entry", false, {102, 103}},
    NamedType{101, "second entry", true, {100}},
};
    return 0;
}
