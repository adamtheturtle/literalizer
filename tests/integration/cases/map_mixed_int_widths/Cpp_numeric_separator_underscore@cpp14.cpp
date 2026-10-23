#include <initializer_list>
#include <string>
#include <map>
int main() {
auto my_data = std::map<std::string, long long>{
    {"a", 1},
    {"b", 1'099'511'627'776},
};
    (void)my_data;
    return 0;
}
