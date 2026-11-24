#include <map>
#include <string>
#include <utility>
int main() {
auto existing = std::map<std::string, std::string>{
    {"_", "_"},
};
auto&& my_data = std::move(existing);
    (void)my_data;
    return 0;
}
