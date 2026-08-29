#include <initializer_list>
#include <string>
#include <map>
#include <vector>
int main() {
auto r = std::map<std::string, int>{
    {"k", 2},
};
auto my_data = std::vector<std::map<std::string, int>>{
    std::map<std::string, int>{{"k", 1}},
    std::move(r),
};
    (void)my_data;
    return 0;
}
