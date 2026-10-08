#include <initializer_list>
#include <string>
#include <map>
#include <vector>
struct Record0 { std::map<std::string, int> input; };
int main() {
auto my_data = std::vector<Record0>{
    Record0{
        {
            {"a", 1},
        },
    },
    Record0{
        {
            {"b", 2},
        },
    },
};
    (void)my_data;
    return 0;
}
