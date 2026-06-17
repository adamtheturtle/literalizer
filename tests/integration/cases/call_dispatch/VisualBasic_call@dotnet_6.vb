Imports System.Collections.Generic
Module Check
    Function put(key As Object, value As Object) As Object
        Return Nothing
    End Function
    Function get(key As Object) As Object
        Return Nothing
    End Function
    Sub _calls()
        put(1, 10)
        get(1)
    End Sub
End Module
