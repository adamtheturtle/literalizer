Imports System.Collections.Generic
Module Check
    Sub _declaration()
        Dim my_data = New Object() {
            42,
            3.14,
            True,
            False,
            "hello ""world"""
        }
    End Sub
    Sub _assignment()
        Dim my_data As Object
        my_data = New Object() {
            42,
            3.14,
            True,
            False,
            "hello ""world"""
        }
    End Sub
End Module
