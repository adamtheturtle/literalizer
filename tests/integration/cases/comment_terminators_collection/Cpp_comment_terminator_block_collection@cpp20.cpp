#include <initializer_list>
#include <string>
#include <vector>
int main() {
auto my_data = std::vector<std::string>{
    /* before first: * / |# -} *) ) =# ]] %} ]# % #> */
    "first",  /* inline first: * / |# -} *) ) =# ]] %} ]# % #> */
    /* before second: * / |# -} *) ) =# ]] %} ]# % #> */
    "second",
    /* trailing: * / |# -} *) ) =# ]] %} ]# % #> */
};
    (void)my_data;
    return 0;
}
