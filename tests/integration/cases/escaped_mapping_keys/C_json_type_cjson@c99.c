#include <cjson/cJSON.h>
int main(void) {
cJSON *_n0 = cJSON_CreateObject();
cJSON *_n1 = cJSON_CreateNumber((double)1);
cJSON_AddItemToObject(_n0, "quote\"backslash\\", _n1);
cJSON *_n2 = cJSON_CreateNumber((double)2);
cJSON_AddItemToObject(_n0, "line\nbreak", _n2);
cJSON *_n3 = cJSON_CreateNumber((double)3);
cJSON_AddItemToObject(_n0, "$(literal)${text}", _n3);
cJSON *_n4 = cJSON_CreateNumber((double)4);
cJSON_AddItemToObject(_n0, "RStr prefix", _n4);
cJSON *my_data = _n0;
    (void)my_data;
    return 0;
}
