#include "../../cpp_support/include/named_type.hpp"
#include <initializer_list>
#include <string>
#include <map>
#include <vector>
int main() {
auto my_data = std::vector<std::map<std::string, std::string>>{
    std::map<std::string, std::string>{{"item", "existing"}},
    // This comment describes the next item.
    std::map<std::string, std::string>{{"item", "next"}},
};
    (void)my_data;
    return 0;
}
