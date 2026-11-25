#include <cjson/cJSON.h>
int main(void) {
cJSON *literalizer_my_data_n0 = cJSON_CreateString("\nroot first line\n  indented\n\nroot last line\n");
cJSON *my_data = literalizer_my_data_n0;
    (void)my_data;
    return 0;
}
