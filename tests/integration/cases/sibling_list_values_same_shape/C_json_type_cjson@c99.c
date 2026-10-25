#include <cjson/cJSON.h>
int main(void) {
cJSON *_n0 = cJSON_CreateObject();
cJSON *_n1 = cJSON_CreateArray();
cJSON *_n2 = cJSON_CreateNumber((double)5);
cJSON_AddItemToArray(_n1, _n2);
cJSON *_n3 = cJSON_CreateArray();
cJSON *_n4 = cJSON_CreateString("compile");
cJSON_AddItemToArray(_n3, _n4);
cJSON *_n5 = cJSON_CreateString("test");
cJSON_AddItemToArray(_n3, _n5);
cJSON_AddItemToArray(_n1, _n3);
cJSON_AddItemToObject(_n0, "test", _n1);
cJSON *_n6 = cJSON_CreateArray();
cJSON *_n7 = cJSON_CreateNumber((double)7);
cJSON_AddItemToArray(_n6, _n7);
cJSON *_n8 = cJSON_CreateArray();
cJSON *_n9 = cJSON_CreateString("link");
cJSON_AddItemToArray(_n8, _n9);
cJSON *_n10 = cJSON_CreateString("test");
cJSON_AddItemToArray(_n8, _n10);
cJSON_AddItemToArray(_n6, _n8);
cJSON_AddItemToObject(_n0, "package", _n6);
cJSON *my_data = _n0;
    (void)my_data;
    return 0;
}
