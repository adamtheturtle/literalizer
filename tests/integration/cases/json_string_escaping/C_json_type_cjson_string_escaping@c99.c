#include <cjson/cJSON.h>
int main(void) {
cJSON *_n0 = cJSON_CreateObject();
cJSON *_n1 = cJSON_CreateString("a\"b\tcé #{world} $ident");
cJSON_AddItemToObject(_n0, "$key", _n1);
cJSON *_n2 = cJSON_CreateString("café");
cJSON_AddItemToObject(_n0, "trailing multi-byte", _n2);
cJSON *my_data = _n0;
    (void)my_data;
    return 0;
}
