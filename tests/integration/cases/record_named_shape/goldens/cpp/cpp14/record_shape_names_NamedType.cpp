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
int main() {
auto my_data = std::vector<NamedType>{
    NamedType{100, "first entry", false, {102, 103}},
    NamedType{101, "second entry", true, {100}},
};
    return 0;
}
