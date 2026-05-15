#include <initializer_list>
#include <string>
#include <map>
#include <vector>
int main() {
auto shared_var = std::map<std::string, std::string>{
    {"_", "_"},
};
auto my_data = std::vector<std::map<std::string, std::string>>{
    std::move(shared_var),
    std::move(shared_var),
};
    (void)my_data;
    return 0;
}
