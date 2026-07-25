#include "../../cpp_support/include/named_type.hpp"
#include <initializer_list>
#include <string>
#include <map>
#include <vector>
struct Record0 { std::string collection; NamedType featured_entry; };
int main() {
auto my_data = Record0{
    "alpha",
    NamedType{
        100,
        "first entry",
        false,
        std::vector<int>{
            102,
            103,
        },
    },
};
    (void)my_data;
    return 0;
}
