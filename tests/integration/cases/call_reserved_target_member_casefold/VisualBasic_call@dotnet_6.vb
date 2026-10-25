Module Check
    Class ObjType_0_
        Public Function BEGIN(a As Object) As Object
            Return Nothing
        End Function
    End Class
    Dim obj As New ObjType_0_()
    Sub _calls()
        obj.BEGIN(42)
    End Sub
End Module
