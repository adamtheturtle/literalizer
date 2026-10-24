#include <cjson/cJSON.h>
int main(void) {
cJSON *_n0 = cJSON_CreateObject();
cJSON *_n1 = cJSON_CreateArray();
cJSON *_n2 = cJSON_CreateArray();
cJSON *_n3 = cJSON_CreateString("nested first line\n  indented\n\nnested last line\n");
cJSON_AddItemToArray(_n2, _n3);
cJSON_AddItemToArray(_n1, _n2);
cJSON_AddItemToObject(_n0, "outer", _n1);
cJSON *my_data = _n0;
    (void)my_data;
    return 0;
}
