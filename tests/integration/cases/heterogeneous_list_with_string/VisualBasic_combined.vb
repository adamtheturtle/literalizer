Imports System.Collections.Generic
Module Check
    Sub _declaration()
        Dim my_data = New Object() {
            "hello",
            42
        }
    End Sub
    Sub _assignment()
        Dim my_data As Object
        my_data = New Object() {
            "hello",
            42
        }
    End Sub
End Module
