module Check exposing (..)


type Val
   = EBool Bool
   | EList (List Val)


my_data : Val
my_data = EList [
   EBool True,
   EBool False,
   EBool True
   ]
