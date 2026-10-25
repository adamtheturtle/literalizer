#include <cjson/cJSON.h>
int main(void) {
cJSON *_n3 = cJSON_CreateArray();
cJSON *_n4 = cJSON_CreateNumber((double)1);
cJSON_AddItemToArray(_n3, _n4);
cJSON *_n5 = cJSON_CreateNumber((double)2);
cJSON_AddItemToArray(_n3, _n5);
cJSON *shared = _n3;
cJSON *_n0 = cJSON_CreateArray();
cJSON *_n1 = cJSON_Duplicate(shared, 1);
cJSON_AddItemToArray(_n0, _n1);
cJSON *_n2 = cJSON_CreateNumber((double)42);
cJSON_AddItemToArray(_n0, _n2);
cJSON *my_data = _n0;
    (void)my_data;
    return 0;
}
