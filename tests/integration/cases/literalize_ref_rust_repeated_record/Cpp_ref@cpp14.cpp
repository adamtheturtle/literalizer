#include <initializer_list>
#include <string>
#include <vector>
struct Record0 { std::vector<int> value; };
int main() {
auto shared = Record0{
    {
        1,
        2,
    },
};
auto my_data = std::vector<Record0>{
    shared,
    shared,
};
    (void)my_data;
    return 0;
}
