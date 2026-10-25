#include <cjson/cJSON.h>
int main(void) {
cJSON *literalizer_my_data_n0 = cJSON_CreateObject();
cJSON *literalizer_my_data_n1 = cJSON_CreateString("a\rb");
cJSON_AddItemToObject(literalizer_my_data_n0, "cr", literalizer_my_data_n1);
cJSON *literalizer_my_data_n2 = cJSON_CreateString("a\r\nb");
cJSON_AddItemToObject(literalizer_my_data_n0, "crlf", literalizer_my_data_n2);
cJSON *literalizer_my_data_n3 = cJSON_CreateString("a\nb");
cJSON_AddItemToObject(literalizer_my_data_n0, "lf", literalizer_my_data_n3);
cJSON *my_data = literalizer_my_data_n0;
    (void)my_data;
    return 0;
}
