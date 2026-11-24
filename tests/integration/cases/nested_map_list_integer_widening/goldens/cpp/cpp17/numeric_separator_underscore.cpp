#include <map>
#include <string>
#include <vector>
int main() {
auto my_data = std::map<std::string, std::vector<long long>>{
    {"a", std::vector<long long>{1}},
    {"b", std::vector<long long>{1'099'511'627'776}},
};
    (void)my_data;
    return 0;
}
