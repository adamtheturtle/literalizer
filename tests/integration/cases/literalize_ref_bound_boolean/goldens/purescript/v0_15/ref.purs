module Check where


data Val
    = PBool Boolean


refFlag :: Val
refFlag = PBool true
my_data :: Val
my_data = refFlag
