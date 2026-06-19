Imports System.Collections.Generic
Module Check
    Function store_item(key As Object, value As Object) As Object
        Return Nothing
    End Function
    Function read_item(key As Object) As Object
        Return Nothing
    End Function
    Sub _calls()
        store_item(1, 10)
        read_item(1)
    End Sub
End Module
