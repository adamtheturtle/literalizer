#include <cjson/cJSON.h>
int main(void) {
cJSON *_n0 = cJSON_CreateArray();
cJSON *_n1 = cJSON_CreateString("]");
cJSON_AddItemToArray(_n0, _n1);
cJSON *_n2 = cJSON_CreateString("a]");
cJSON_AddItemToArray(_n0, _n2);
cJSON *_n3 = cJSON_CreateString("a]=");
cJSON_AddItemToArray(_n0, _n3);
cJSON *_n4 = cJSON_CreateString("a]b");
cJSON_AddItemToArray(_n0, _n4);
cJSON *my_data = _n0;
    (void)my_data;
    return 0;
}
