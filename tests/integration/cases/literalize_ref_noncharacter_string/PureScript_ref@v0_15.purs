module Check where


data Val
    = PStr String


sourceValue :: Val
sourceValue = PStr "￾￿"
my_data :: Val
my_data = sourceValue
