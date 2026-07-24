#include "../../cpp_support/include/named_map.hpp"
#include <initializer_list>
#include <string>
#include <map>
#include <vector>
int main() {
auto my_data = std::vector<NamedMap>{
    std::map<std::string, std::string>{{"expense_id", "001"}, {"vendor", "restaurant"}},
    std::map<std::string, std::string>{{"expense_id", "002"}, {"vendor", "retailer"}},
};
    (void)my_data;
    return 0;
}
