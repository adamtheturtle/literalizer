#include <cjson/cJSON.h>
int main(void) {
cJSON *_n0 = cJSON_CreateObject();
cJSON *_n1 = cJSON_CreateArray();
cJSON *_n2 = cJSON_CreateObject();
cJSON *_n3 = cJSON_CreateArray();
cJSON *_n4 = cJSON_CreateNumber((double)1);
cJSON_AddItemToArray(_n3, _n4);
cJSON_AddItemToObject(_n2, "item", _n3);
cJSON_AddItemToArray(_n1, _n2);
cJSON_AddItemToObject(_n0, "a", _n1);
cJSON *_n5 = cJSON_CreateArray();
cJSON *_n6 = cJSON_CreateObject();
cJSON *_n7 = cJSON_CreateArray();
cJSON *_n8 = cJSON_CreateNumber((double)2);
cJSON_AddItemToArray(_n7, _n8);
cJSON_AddItemToObject(_n6, "item", _n7);
cJSON_AddItemToArray(_n5, _n6);
cJSON_AddItemToObject(_n0, "b", _n5);
cJSON *my_data = _n0;
    (void)my_data;
    return 0;
}
