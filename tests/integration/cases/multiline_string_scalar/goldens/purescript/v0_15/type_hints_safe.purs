module Check where


data Val
    = PStr String


my_data :: Val
my_data = PStr "\nroot first line\n  indented\n\nroot last line\n"
