#include "../../cpp_support/include/named_type.hpp"
#include <map>
#include <string>
#include <vector>
int main() {
auto my_data = std::vector<ExternalRecordShape>{
    std::map<std::string, std::string>{{"first", "Alice"}, {"last", "Smith"}},
    std::map<std::string, std::string>{{"first", "Bob"}, {"last", "Jones"}},
};
    return 0;
}
