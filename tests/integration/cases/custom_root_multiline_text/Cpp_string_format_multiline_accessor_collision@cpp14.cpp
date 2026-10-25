#include <initializer_list>
#include <string>
int main() {
const auto* fixtureRoot = R"(head
final my_data = 123;
final fakeRoot = 1;
final fixtureRoot = 1;
tail)";
    (void)fixtureRoot;
    return 0;
}
