#include <initializer_list>
#include <string>
#include <vector>
#include <utility>
struct Record1 { std::vector<int> numbers; std::vector<std::string> strings; };
struct Record0 { std::vector<std::pair<std::string, int>> omap_value; Record1 sibling_lists; std::vector<std::string> ref_marker_present; };
int main() {
auto my_data = Record0{
    {
        {"first", 1},
    },
    {
        {
            1,
            2,
        },
        {
            "x",
            "y",
        },
    },
    {
        "$keep",
        "z",
    },
};
    (void)my_data;
    return 0;
}
