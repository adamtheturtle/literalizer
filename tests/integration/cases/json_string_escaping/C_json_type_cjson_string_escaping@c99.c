#include <cjson/cJSON.h>
int main(void) {
cJSON *literalizer_my_data_n0 = cJSON_CreateObject();
cJSON *literalizer_my_data_n1 = cJSON_CreateString("a\"b\tcé #{world} $ident");
cJSON_AddItemToObject(literalizer_my_data_n0, "$key", literalizer_my_data_n1);
cJSON *literalizer_my_data_n2 = cJSON_CreateString("café");
cJSON_AddItemToObject(literalizer_my_data_n0, "trailing multi-byte", literalizer_my_data_n2);
cJSON *my_data = literalizer_my_data_n0;
    (void)my_data;
    return 0;
}
