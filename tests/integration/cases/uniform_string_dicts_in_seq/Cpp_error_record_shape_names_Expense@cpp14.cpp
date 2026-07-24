#include "../../cpp_support/include/expense.hpp"
#include <initializer_list>
#include <string>
#include <map>
#include <vector>
int main() {
auto my_data = std::vector<Expense>{
    std::map<std::string, std::string>{{"first", "Alice"}, {"last", "Smith"}},
    std::map<std::string, std::string>{{"first", "Bob"}, {"last", "Jones"}},
};
    (void)my_data;
    return 0;
}
