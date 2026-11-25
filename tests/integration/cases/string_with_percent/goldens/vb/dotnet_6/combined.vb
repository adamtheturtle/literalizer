Imports System.Collections.Generic
Module Check
    Sub _declaration()
        Dim my_data = New String() {
            "100% done",
            "%(name) is here"
        }
    End Sub
    Sub _assignment()
        Dim my_data As Object
        my_data = New String() {
            "100% done",
            "%(name) is here"
        }
    End Sub
End Module
