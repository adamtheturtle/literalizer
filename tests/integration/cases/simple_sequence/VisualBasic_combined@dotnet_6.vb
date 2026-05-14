Imports System.Collections.Generic
Module Check
    Sub _declaration()
        Dim my_data = New Object() {
            1,
            "hello",
            True,
            Nothing
        }
    End Sub
    Sub _assignment()
        Dim my_data As Object
        my_data = New Object() {
            1,
            "hello",
            True,
            Nothing
        }
    End Sub
End Module
