#include <map>
#include <string>
#include <utility>
int main() {
auto my_var = std::map<std::string, std::string>{
    {"_", "_"},
};
auto&& my_data = std::move(my_var);
    (void)my_data;
    return 0;
}
