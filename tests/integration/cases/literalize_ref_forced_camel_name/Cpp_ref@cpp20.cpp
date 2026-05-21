#include <initializer_list>
#include <string>
#include <map>
int main() {
auto userObj = std::map<std::string, std::string>{
    {"_", "_"},
};
auto my_data = std::move(userObj);
    (void)my_data;
    return 0;
}
