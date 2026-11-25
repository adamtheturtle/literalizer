module Check exposing (..)


type Val
    = EList (List Val)


-- empty heading
-- empty body
-- after empty
my_data : Val
my_data = EList []
