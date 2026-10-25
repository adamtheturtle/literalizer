#include <cjson/cJSON.h>
int main(void) {
cJSON *_n0 = cJSON_CreateObject();
cJSON *_n1 = cJSON_CreateArray();
cJSON *_n2 = cJSON_CreateNumber((double)1);
cJSON_AddItemToArray(_n1, _n2);
cJSON *_n3 = cJSON_CreateNumber((double)2);
cJSON_AddItemToArray(_n1, _n3);
cJSON_AddItemToObject(_n0, "field", _n1);
cJSON *shared = _n0;
cJSON * my_data = shared;
    (void)my_data;
    return 0;
}
