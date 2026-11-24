module Check where


data Val
    = PNull
    | PInt Int
    | PList (Array Val)


myValue :: Val
myValue = PNull
my_data :: Val
my_data = myValue
