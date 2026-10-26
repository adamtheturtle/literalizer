#include <map>
#include <string>
#include <utility>
int main() {
auto user_obj = std::map<std::string, std::string>{
    {"_", "_"},
};
auto&& my_data = std::move(user_obj);
    (void)my_data;
    return 0;
}
