Module Check
    Class ObjType_0_
        Public Function class(a As Object) As Object
            Return Nothing
        End Function
    End Class
    Dim obj As New ObjType_0_()
    Sub _calls()
        obj.class(42)
    End Sub
End Module
