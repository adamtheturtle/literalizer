#include "../../cpp_support/include/named_type.hpp"
#include <string>
struct Record0 { std::string collection; NamedType featured_entry; };
int main() {
auto my_data = Record0{
    "alpha",
    {
        100,
        "first entry",
        false,
        {
            102,
            103,
        },
    },
};
    return 0;
}
