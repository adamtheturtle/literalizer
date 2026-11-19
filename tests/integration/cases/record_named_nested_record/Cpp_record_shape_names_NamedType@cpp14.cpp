#include <string>
#include <vector>
struct FixtureRecord0 { int id{}; std::string label; bool enabled{}; std::vector<int> related_ids; };
using NamedType = decltype(FixtureRecord0{
    1,
    "x",
    true,
    {
        0,
    },
});
struct Record0 { std::string collection; NamedType featured_entry; };
int main() {
auto my_data = Record0{
    "alpha",
    {
        100,
        "first entry",
        false,
        {
            102,
            103,
        },
    },
};
    return 0;
}
