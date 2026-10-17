#include <initializer_list>
#include <string>
#include <map>
int main() {
auto my_data = std::map<std::string, std::string>{
    // server
    {"host", "localhost"},  // default
};
    (void)my_data;
    return 0;
}
