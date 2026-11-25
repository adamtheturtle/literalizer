Imports System.Collections.Generic
Module Check
    Sub _declaration()
        ' first
        ' second
        Dim my_data = New String() {
            "a",
            "b"
        }
    End Sub
    Sub _assignment()
        Dim my_data As Object
        ' first
        ' second
        my_data = New String() {
            "a",
            "b"
        }
    End Sub
End Module
