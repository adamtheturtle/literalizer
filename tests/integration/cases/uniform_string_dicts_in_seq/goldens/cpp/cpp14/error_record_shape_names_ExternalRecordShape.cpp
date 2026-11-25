#include <map>
#include <string>
using ExternalRecordShape = decltype(std::map<std::string, std::string>{
    {"first", ""},
    {"last", ""},
});
#include <vector>
int main() {
auto my_data = std::vector<ExternalRecordShape>{
    std::map<std::string, std::string>{{"first", "Alice"}, {"last", "Smith"}},
    std::map<std::string, std::string>{{"first", "Bob"}, {"last", "Jones"}},
};
    return 0;
}
