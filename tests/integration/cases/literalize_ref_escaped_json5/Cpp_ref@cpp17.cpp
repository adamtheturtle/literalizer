#include <initializer_list>
#include <string>
#include <map>
int main() {
auto existing = std::map<std::string, std::string>{
    {"_", "_"},
};
auto my_data = std::move(existing);
    (void)my_data;
    return 0;
}
