#include <map>
#include <string>
int main() {
auto my_data = std::map<std::string, std::string>{
    {"key", "\"bang!\""},  // real
};
    (void)my_data;
    return 0;
}
