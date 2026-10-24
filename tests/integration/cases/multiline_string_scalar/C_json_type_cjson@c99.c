#include <cjson/cJSON.h>
int main(void) {
cJSON *_n0 = cJSON_CreateString("\nroot first line\n  indented\n\nroot last line\n");
cJSON *my_data = _n0;
    (void)my_data;
    return 0;
}
