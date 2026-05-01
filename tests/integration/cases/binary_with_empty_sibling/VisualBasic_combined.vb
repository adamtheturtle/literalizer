Imports System.Collections.Generic
Module Check
    Sub _declaration()
        Dim my_data = New Object() {
            "48656c6c6f",
            New Object() {}
        }
    End Sub
    Sub _assignment()
        Dim my_data As Object
        my_data = New Object() {
            "48656c6c6f",
            New Object() {}
        }
    End Sub
End Module
