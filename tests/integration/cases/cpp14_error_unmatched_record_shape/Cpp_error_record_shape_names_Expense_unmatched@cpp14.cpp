#include "../../cpp_support/include/expense.hpp"
#include <initializer_list>
#include <string>
#include <map>
#include <vector>
int main() {
auto my_data = std::vector<std::map<std::string, std::string>>{
    std::map<std::string, std::string>{{"expense_id", "001"}, {"trip_id", "001"}, {"currency", "USD"}},
    std::map<std::string, std::string>{{"expense_id", "002"}, {"trip_id", "001"}, {"currency", "USD"}},
};
    (void)my_data;
    return 0;
}
