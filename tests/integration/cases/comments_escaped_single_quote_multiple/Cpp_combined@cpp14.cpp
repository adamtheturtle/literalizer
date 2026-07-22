#include <initializer_list>
#include <string>
#include <map>
struct Record0 { std::string host; int port{}; };
int main() {
auto my_data = Record0{
    "it's here",  // a comment
    80,  // another
};
(void)my_data;
my_data = Record0{
    "it's here",  // a comment
    80,  // another
};
    (void)my_data;
    return 0;
}
