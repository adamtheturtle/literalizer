#include <map>
#include <string>
int main() {
auto my_data = std::map<std::string, std::string>{
    // server
    {"host", "localhost"},  // default
};
    (void)my_data;
    return 0;
}
