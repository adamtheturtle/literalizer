#include <initializer_list>
#include <vector>
int main() {
auto my_data = std::vector<bool>{
   true,
   false,
   true,
};
   (void)my_data;
   return 0;
}
