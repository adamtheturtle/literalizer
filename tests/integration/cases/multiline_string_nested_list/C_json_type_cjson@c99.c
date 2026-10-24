#include <cjson/cJSON.h>
int main(void) {
cJSON *_n0 = cJSON_CreateArray();
cJSON *_n1 = cJSON_CreateArray();
cJSON *_n2 = cJSON_CreateString("\nfirst line\n  indented\n\nlast line\n");
cJSON_AddItemToArray(_n1, _n2);
cJSON_AddItemToArray(_n0, _n1);
cJSON *my_data = _n0;
    (void)my_data;
    return 0;
}
