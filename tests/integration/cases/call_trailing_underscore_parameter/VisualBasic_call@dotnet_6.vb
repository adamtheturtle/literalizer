Imports System.Collections.Generic
Module Check
    Function do_thing(x_ As Object) As Object
        Return Nothing
    End Function
    Sub _calls()
        do_thing(1)
        do_thing(2)
    End Sub
End Module
