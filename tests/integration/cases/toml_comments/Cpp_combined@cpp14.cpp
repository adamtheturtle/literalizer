#include <initializer_list>
#include <string>
#include <map>
struct Record0 { int answer{}; std::string plain; };
int main() {
auto my_data = Record0{
    // before
    42,  // inline
    "ok",
    // trailing
};
(void)my_data;
my_data = Record0{
    // before
    42,  // inline
    "ok",
    // trailing
};
    (void)my_data;
    return 0;
}
