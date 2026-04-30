#include <initializer_list>
#include <string>
#include <map>
int main() {
const auto my_data = std::map<std::string, std::string>{
    {"key", "\"bang!\""},  // real
};
    (void)my_data;
    return 0;
}
