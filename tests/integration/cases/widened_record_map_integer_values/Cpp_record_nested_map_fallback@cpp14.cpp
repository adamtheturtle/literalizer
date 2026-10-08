#include <initializer_list>
#include <string>
#include <map>
#include <vector>
using LiteralizerRecordValue = Value;
struct Record0 { std::map<std::string, LiteralizerRecordValue> input; };
int main() {
auto my_data = std::vector<Record0>{
    Record0{{{"a", Value{1}}}},
    Record0{{{"b", Value{2}}}},
};
    (void)my_data;
    return 0;
}
