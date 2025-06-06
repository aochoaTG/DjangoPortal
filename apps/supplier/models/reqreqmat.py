from django.db import models

class ReqReqMat(models.Model):
    id_req_mat      = models.IntegerField(primary_key=True, verbose_name="ID de Requisición")
    id_usr          = models.IntegerField(verbose_name="ID de Usuario") # Id del usuario que solicita
    id_nota         = models.IntegerField(verbose_name="ID de Nota")
    id_emp_sol      = models.IntegerField(verbose_name="ID del Solicitante") # Id del empleado que solicita
    id_emp_dir      = models.IntegerField(verbose_name="ID del Empleado Dirigido") # Id del empleado al que vá dirigido
    id_emp_apr      = models.IntegerField(verbose_name="ID del Aprobador")
    id_tip_doc      = models.IntegerField(verbose_name="ID del Tipo de Documento")
    num_doc         = models.IntegerField(unique=True, verbose_name="Número de Documento")
    fec_doc         = models.DateTimeField(verbose_name="Fecha del Documento")
    fec_req         = models.DateTimeField(verbose_name="Fecha de Requisición")
    fec_apr         = models.DateTimeField(verbose_name="Fecha de Aprobación")
    sub             = models.FloatField(verbose_name="Subtotal")
    imps            = models.FloatField(verbose_name="Impuestos")
    total           = models.FloatField(verbose_name="Total")
    ref             = models.CharField(max_length=200, null=True, blank=True, verbose_name="Referencia")
    status          = models.PositiveSmallIntegerField(verbose_name="Estatus")
    id_cpt          = models.IntegerField(verbose_name="ID de Concepto")
    c_rec           = models.PositiveSmallIntegerField(verbose_name="Cantidad Recibida")
    c_lib           = models.PositiveSmallIntegerField(verbose_name="Cantidad Liberada")
    id_suc          = models.IntegerField(verbose_name="ID de Sucursal")
    id_sesion       = models.IntegerField(verbose_name="ID de Sesión")
    fec_reg_lib_cot = models.DateTimeField(verbose_name="Fecha de Registro de Liberación de Cotización")
    id_emp_lib_cot  = models.IntegerField(verbose_name="ID del Empleado que Liberó la Cotización")
    fec_reg_lib_apr = models.DateTimeField(verbose_name="Fecha de Registro de Liberación de Aprobación")
    id_emp_lib_apr  = models.IntegerField(verbose_name="ID del Empleado que Liberó la Aprobación")
    id_mda          = models.IntegerField(verbose_name="ID de Moneda")
    oper            = models.PositiveSmallIntegerField(verbose_name="Operación")
    tc              = models.FloatField(verbose_name="Tipo de Cambio")
    id_nota_desl    = models.BigIntegerField(verbose_name="ID de Nota de Deslinde")

    class Meta:
        db_table = 'req_req_mat'  # Especifica el nombre exacto de la tabla en la base de datos
        unique_together = (('id_tip_doc', 'num_doc'),)  # Índice único IX_tip_doc_num_doc
        managed = False  # Indica que Django no debe intentar modificar esta tabla
        verbose_name = "Requisición de Material"
        verbose_name_plural = "Requisiciones de Material"

    def __str__(self):
        return f"Requisición {self.id_req_mat}"

    def get_all_requisitions(self):
        # Consulta SQL personalizada
        sql_query = """
            SELECT 'Diaz Gas' Empresa, '1G_TOTALGAS' Company, t8.Lineas, t8.TotalCosto, t1.id_req_mat Folio, t1.fec_req FechaRequisicion, t2.nom usuarioSolicita, t3.nom empleadoSolicita, t4.nom dirigidoA, t1.ref Referencia, t5.des Estado, t6.nom empleadoLibero, t1.fec_reg_lib_cot Fecha_liberacion, t7.nom Cotizó, t1.fec_reg_lib_apr, t1.*
            FROM
                [1G_TOTALGAS].[dbo].[req_req_mat] t1 WITH (NOLOCK) LEFT JOIN [1G_TOTALGAS].[dbo].[vt_usr] t2 WITH (NOLOCK) ON t1.id_usr = t2.id_usr	LEFT JOIN [1G_TOTALGAS].[dbo].[vt_usr] t3 ON t1.id_emp_sol = t3.id_emp
                LEFT JOIN [1G_TOTALGAS].[dbo].[vt_usr] t4 WITH (NOLOCK) ON t1.id_emp_dir = t4.id_emp LEFT JOIN [1G_TOTALGAS].[dbo].[vt_status_req] t5 WITH (NOLOCK) ON t1.status = t5.id_status
                LEFT JOIN [1G_TOTALGAS].[dbo].[vt_usr] t6 WITH (NOLOCK) ON t1.id_emp_lib_cot = t6.id_usr LEFT JOIN [1G_TOTALGAS].[dbo].[vt_usr] t7 WITH (NOLOCK) ON t1.id_emp_lib_apr = t7.id_usr
                LEFT JOIN (SELECT id_req_mat, SUM(total) TotalCosto, COUNT(*) Lineas FROM [1G_TOTALGAS].[dbo].[req_req_mat_det] GROUP BY id_req_mat) t8 ON t1.id_req_mat = t8.id_req_mat    
            WHERE t1.fec_req >= '2023-06-01'
            UNION
            SELECT 'Villa Ahumada' Empresa, '1G_TGS_AHUMADA' Company, t8.Lineas, t8.TotalCosto, t1.id_req_mat Folio, t1.fec_req FechaRequisicion, t2.nom usuarioSolicita, t3.nom empleadoSolicita, t4.nom dirigidoA, t1.ref Referencia, t5.des Estado, t6.nom empleadoLibero, t1.fec_reg_lib_cot Fecha_liberacion, t7.nom Cotizó, t1.fec_reg_lib_apr, t1.*
            FROM
                [1G_TGS_AHUMADA].[dbo].[req_req_mat] t1 WITH (NOLOCK) LEFT JOIN [1G_TGS_AHUMADA].[dbo].[vt_usr] t2 WITH (NOLOCK) ON t1.id_usr = t2.id_usr	LEFT JOIN [1G_TGS_AHUMADA].[dbo].[vt_usr] t3 ON t1.id_emp_sol = t3.id_emp
                LEFT JOIN [1G_TGS_AHUMADA].[dbo].[vt_usr] t4 WITH (NOLOCK) ON t1.id_emp_dir = t4.id_emp LEFT JOIN [1G_TGS_AHUMADA].[dbo].[vt_status_req] t5 WITH (NOLOCK) ON t1.status = t5.id_status
                LEFT JOIN [1G_TGS_AHUMADA].[dbo].[vt_usr] t6 WITH (NOLOCK) ON t1.id_emp_lib_cot = t6.id_usr LEFT JOIN [1G_TGS_AHUMADA].[dbo].[vt_usr] t7 WITH (NOLOCK) ON t1.id_emp_lib_apr = t7.id_usr
                LEFT JOIN (SELECT id_req_mat, SUM(total) TotalCosto, COUNT(*) Lineas FROM [1G_TGS_AHUMADA].[dbo].[req_req_mat_det] GROUP BY id_req_mat) t8 ON t1.id_req_mat = t8.id_req_mat    
            WHERE t1.fec_req >= '2023-06-01'
            UNION
            SELECT 'Castaño' Empresa, '1G_TGS_CASTANO' Company, t8.Lineas, t8.TotalCosto, t1.id_req_mat Folio, t1.fec_req FechaRequisicion, t2.nom usuarioSolicita, t3.nom empleadoSolicita, t4.nom dirigidoA, t1.ref Referencia, t5.des Estado, t6.nom empleadoLibero, t1.fec_reg_lib_cot Fecha_liberacion, t7.nom Cotizó, t1.fec_reg_lib_apr, t1.*
            FROM
                [1G_TGS_CASTANO].[dbo].[req_req_mat] t1 WITH (NOLOCK) LEFT JOIN [1G_TGS_CASTANO].[dbo].[vt_usr] t2 WITH (NOLOCK) ON t1.id_usr = t2.id_usr	LEFT JOIN [1G_TGS_CASTANO].[dbo].[vt_usr] t3 ON t1.id_emp_sol = t3.id_emp
                LEFT JOIN [1G_TGS_CASTANO].[dbo].[vt_usr] t4 WITH (NOLOCK) ON t1.id_emp_dir = t4.id_emp LEFT JOIN [1G_TGS_CASTANO].[dbo].[vt_status_req] t5 WITH (NOLOCK) ON t1.status = t5.id_status
                LEFT JOIN [1G_TGS_CASTANO].[dbo].[vt_usr] t6 WITH (NOLOCK) ON t1.id_emp_lib_cot = t6.id_usr LEFT JOIN [1G_TGS_CASTANO].[dbo].[vt_usr] t7 WITH (NOLOCK) ON t1.id_emp_lib_apr = t7.id_usr
                LEFT JOIN (SELECT id_req_mat, SUM(total) TotalCosto, COUNT(*) Lineas FROM [1G_TGS_CASTANO].[dbo].[req_req_mat_det] GROUP BY id_req_mat) t8 ON t1.id_req_mat = t8.id_req_mat    
            WHERE t1.fec_req >= '2023-06-01'
            UNION
            SELECT 'Clara' Empresa, '1G_TGS_CLARA' Company, t8.Lineas, t8.TotalCosto, t1.id_req_mat Folio, t1.fec_req FechaRequisicion, t2.nom usuarioSolicita, t3.nom empleadoSolicita, t4.nom dirigidoA, t1.ref Referencia, t5.des Estado, t6.nom empleadoLibero, t1.fec_reg_lib_cot Fecha_liberacion, t7.nom Cotizó, t1.fec_reg_lib_apr, t1.*
            FROM
                [1G_TGS_CLARA].[dbo].[req_req_mat] t1 WITH (NOLOCK) LEFT JOIN [1G_TGS_CLARA].[dbo].[vt_usr] t2 WITH (NOLOCK) ON t1.id_usr = t2.id_usr	LEFT JOIN [1G_TGS_CLARA].[dbo].[vt_usr] t3 ON t1.id_emp_sol = t3.id_emp
                LEFT JOIN [1G_TGS_CLARA].[dbo].[vt_usr] t4 WITH (NOLOCK) ON t1.id_emp_dir = t4.id_emp LEFT JOIN [1G_TGS_CLARA].[dbo].[vt_status_req] t5 WITH (NOLOCK) ON t1.status = t5.id_status
                LEFT JOIN [1G_TGS_CLARA].[dbo].[vt_usr] t6 WITH (NOLOCK) ON t1.id_emp_lib_cot = t6.id_usr LEFT JOIN [1G_TGS_CLARA].[dbo].[vt_usr] t7 WITH (NOLOCK) ON t1.id_emp_lib_apr = t7.id_usr
                LEFT JOIN (SELECT id_req_mat, SUM(total) TotalCosto, COUNT(*) Lineas FROM [1G_TGS_CLARA].[dbo].[req_req_mat_det] GROUP BY id_req_mat) t8 ON t1.id_req_mat = t8.id_req_mat    
            WHERE t1.fec_req >= '2023-06-01'
            UNION
            SELECT 'Gasomex' Empresa, '1G_TGS_GASOMEX' Company, t8.Lineas, t8.TotalCosto, t1.id_req_mat Folio, t1.fec_req FechaRequisicion, t2.nom usuarioSolicita, t3.nom empleadoSolicita, t4.nom dirigidoA, t1.ref Referencia, t5.des Estado, t6.nom empleadoLibero, t1.fec_reg_lib_cot Fecha_liberacion, t7.nom Cotizó, t1.fec_reg_lib_apr, t1.*
            FROM
                [1G_TGS_GASOMEX].[dbo].[req_req_mat] t1 WITH (NOLOCK) LEFT JOIN [1G_TGS_GASOMEX].[dbo].[vt_usr] t2 WITH (NOLOCK) ON t1.id_usr = t2.id_usr	LEFT JOIN [1G_TGS_GASOMEX].[dbo].[vt_usr] t3 ON t1.id_emp_sol = t3.id_emp
                LEFT JOIN [1G_TGS_GASOMEX].[dbo].[vt_usr] t4 WITH (NOLOCK) ON t1.id_emp_dir = t4.id_emp LEFT JOIN [1G_TGS_GASOMEX].[dbo].[vt_status_req] t5 WITH (NOLOCK) ON t1.status = t5.id_status
                LEFT JOIN [1G_TGS_GASOMEX].[dbo].[vt_usr] t6 WITH (NOLOCK) ON t1.id_emp_lib_cot = t6.id_usr LEFT JOIN [1G_TGS_GASOMEX].[dbo].[vt_usr] t7 WITH (NOLOCK) ON t1.id_emp_lib_apr = t7.id_usr
                LEFT JOIN (SELECT id_req_mat, SUM(total) TotalCosto, COUNT(*) Lineas FROM [1G_TGS_GASOMEX].[dbo].[req_req_mat_det] GROUP BY id_req_mat) t8 ON t1.id_req_mat = t8.id_req_mat    
            WHERE t1.fec_req >= '2023-06-01'
            UNION
            SELECT 'INMO' Empresa, '1G_TGS_INMO' Company, t8.Lineas, t8.TotalCosto, t1.id_req_mat Folio, t1.fec_req FechaRequisicion, t2.nom usuarioSolicita, t3.nom empleadoSolicita, t4.nom dirigidoA, t1.ref Referencia, t5.des Estado, t6.nom empleadoLibero, t1.fec_reg_lib_cot Fecha_liberacion, t7.nom Cotizó, t1.fec_reg_lib_apr, t1.*
            FROM
                [1G_TGS_INMO].[dbo].[req_req_mat] t1 WITH (NOLOCK) LEFT JOIN [1G_TGS_INMO].[dbo].[vt_usr] t2 WITH (NOLOCK) ON t1.id_usr = t2.id_usr	LEFT JOIN [1G_TGS_INMO].[dbo].[vt_usr] t3 ON t1.id_emp_sol = t3.id_emp
                LEFT JOIN [1G_TGS_INMO].[dbo].[vt_usr] t4 WITH (NOLOCK) ON t1.id_emp_dir = t4.id_emp LEFT JOIN [1G_TGS_INMO].[dbo].[vt_status_req] t5 WITH (NOLOCK) ON t1.status = t5.id_status
                LEFT JOIN [1G_TGS_INMO].[dbo].[vt_usr] t6 WITH (NOLOCK) ON t1.id_emp_lib_cot = t6.id_usr LEFT JOIN [1G_TGS_INMO].[dbo].[vt_usr] t7 WITH (NOLOCK) ON t1.id_emp_lib_apr = t7.id_usr
                LEFT JOIN (SELECT id_req_mat, SUM(total) TotalCosto, COUNT(*) Lineas FROM [1G_TGS_INMO].[dbo].[req_req_mat_det] GROUP BY id_req_mat) t8 ON t1.id_req_mat = t8.id_req_mat    
            WHERE t1.fec_req >= '2023-06-01'
            UNION
            SELECT 'Jarudo' Empresa, '1G_TGS_JARUDO' Company, t8.Lineas, t8.TotalCosto, t1.id_req_mat Folio, t1.fec_req FechaRequisicion, t2.nom usuarioSolicita, t3.nom empleadoSolicita, t4.nom dirigidoA, t1.ref Referencia, t5.des Estado, t6.nom empleadoLibero, t1.fec_reg_lib_cot Fecha_liberacion, t7.nom Cotizó, t1.fec_reg_lib_apr, t1.*
            FROM
                [1G_TGS_JARUDO].[dbo].[req_req_mat] t1 WITH (NOLOCK) LEFT JOIN [1G_TGS_JARUDO].[dbo].[vt_usr] t2 WITH (NOLOCK) ON t1.id_usr = t2.id_usr	LEFT JOIN [1G_TGS_JARUDO].[dbo].[vt_usr] t3 ON t1.id_emp_sol = t3.id_emp
                LEFT JOIN [1G_TGS_JARUDO].[dbo].[vt_usr] t4 WITH (NOLOCK) ON t1.id_emp_dir = t4.id_emp LEFT JOIN [1G_TGS_JARUDO].[dbo].[vt_status_req] t5 WITH (NOLOCK) ON t1.status = t5.id_status
                LEFT JOIN [1G_TGS_JARUDO].[dbo].[vt_usr] t6 WITH (NOLOCK) ON t1.id_emp_lib_cot = t6.id_usr LEFT JOIN [1G_TGS_JARUDO].[dbo].[vt_usr] t7 WITH (NOLOCK) ON t1.id_emp_lib_apr = t7.id_usr
                LEFT JOIN (SELECT id_req_mat, SUM(total) TotalCosto, COUNT(*) Lineas FROM [1G_TGS_JARUDO].[dbo].[req_req_mat_det] GROUP BY id_req_mat) t8 ON t1.id_req_mat = t8.id_req_mat    
            WHERE t1.fec_req >= '2023-06-01'
            UNION
            SELECT 'Petrotal' Empresa, '1G_TGS_PETROTAL' Company, t8.Lineas, t8.TotalCosto, t1.id_req_mat Folio, t1.fec_req FechaRequisicion, t2.nom usuarioSolicita, t3.nom empleadoSolicita, t4.nom dirigidoA, t1.ref Referencia, t5.des Estado, t6.nom empleadoLibero, t1.fec_reg_lib_cot Fecha_liberacion, t7.nom Cotizó, t1.fec_reg_lib_apr, t1.*
            FROM
                [1G_TGS_PETROTAL].[dbo].[req_req_mat] t1 WITH (NOLOCK) LEFT JOIN [1G_TGS_PETROTAL].[dbo].[vt_usr] t2 WITH (NOLOCK) ON t1.id_usr = t2.id_usr	LEFT JOIN [1G_TGS_PETROTAL].[dbo].[vt_usr] t3 ON t1.id_emp_sol = t3.id_emp
                LEFT JOIN [1G_TGS_PETROTAL].[dbo].[vt_usr] t4 WITH (NOLOCK) ON t1.id_emp_dir = t4.id_emp LEFT JOIN [1G_TGS_PETROTAL].[dbo].[vt_status_req] t5 WITH (NOLOCK) ON t1.status = t5.id_status
                LEFT JOIN [1G_TGS_PETROTAL].[dbo].[vt_usr] t6 WITH (NOLOCK) ON t1.id_emp_lib_cot = t6.id_usr LEFT JOIN [1G_TGS_PETROTAL].[dbo].[vt_usr] t7 WITH (NOLOCK) ON t1.id_emp_lib_apr = t7.id_usr
                LEFT JOIN (SELECT id_req_mat, SUM(total) TotalCosto, COUNT(*) Lineas FROM [1G_TGS_PETROTAL].[dbo].[req_req_mat_det] GROUP BY id_req_mat) t8 ON t1.id_req_mat = t8.id_req_mat    
            WHERE t1.fec_req >= '2023-06-01'
            UNION
            SELECT 'Picachos' Empresa, '1G_TGS_PICACHOS' Company, t8.Lineas, t8.TotalCosto, t1.id_req_mat Folio, t1.fec_req FechaRequisicion, t2.nom usuarioSolicita, t3.nom empleadoSolicita, t4.nom dirigidoA, t1.ref Referencia, t5.des Estado, t6.nom empleadoLibero, t1.fec_reg_lib_cot Fecha_liberacion, t7.nom Cotizó, t1.fec_reg_lib_apr, t1.*
            FROM
                [1G_TGS_PICACHOS].[dbo].[req_req_mat] t1 WITH (NOLOCK) LEFT JOIN [1G_TGS_PICACHOS].[dbo].[vt_usr] t2 WITH (NOLOCK) ON t1.id_usr = t2.id_usr	LEFT JOIN [1G_TGS_PICACHOS].[dbo].[vt_usr] t3 ON t1.id_emp_sol = t3.id_emp
                LEFT JOIN [1G_TGS_PICACHOS].[dbo].[vt_usr] t4 WITH (NOLOCK) ON t1.id_emp_dir = t4.id_emp LEFT JOIN [1G_TGS_PICACHOS].[dbo].[vt_status_req] t5 WITH (NOLOCK) ON t1.status = t5.id_status
                LEFT JOIN [1G_TGS_PICACHOS].[dbo].[vt_usr] t6 WITH (NOLOCK) ON t1.id_emp_lib_cot = t6.id_usr LEFT JOIN [1G_TGS_PICACHOS].[dbo].[vt_usr] t7 WITH (NOLOCK) ON t1.id_emp_lib_apr = t7.id_usr
                LEFT JOIN (SELECT id_req_mat, SUM(total) TotalCosto, COUNT(*) Lineas FROM [1G_TGS_PICACHOS].[dbo].[req_req_mat_det] GROUP BY id_req_mat) t8 ON t1.id_req_mat = t8.id_req_mat    
            WHERE t1.fec_req >= '2023-06-01'
            UNION
            SELECT 'SYC' Empresa, '1G_TGS_SERVICIOSYC' Company, t8.Lineas, t8.TotalCosto, t1.id_req_mat Folio, t1.fec_req FechaRequisicion, t2.nom usuarioSolicita, t3.nom empleadoSolicita, t4.nom dirigidoA, t1.ref Referencia, t5.des Estado, t6.nom empleadoLibero, t1.fec_reg_lib_cot Fecha_liberacion, t7.nom Cotizó, t1.fec_reg_lib_apr, t1.*
            FROM
                [1G_TGS_SERVICIOSYC].[dbo].[req_req_mat] t1 WITH (NOLOCK) LEFT JOIN [1G_TGS_SERVICIOSYC].[dbo].[vt_usr] t2 WITH (NOLOCK) ON t1.id_usr = t2.id_usr	LEFT JOIN [1G_TGS_SERVICIOSYC].[dbo].[vt_usr] t3 ON t1.id_emp_sol = t3.id_emp
                LEFT JOIN [1G_TGS_SERVICIOSYC].[dbo].[vt_usr] t4 WITH (NOLOCK) ON t1.id_emp_dir = t4.id_emp LEFT JOIN [1G_TGS_SERVICIOSYC].[dbo].[vt_status_req] t5 WITH (NOLOCK) ON t1.status = t5.id_status
                LEFT JOIN [1G_TGS_SERVICIOSYC].[dbo].[vt_usr] t6 WITH (NOLOCK) ON t1.id_emp_lib_cot = t6.id_usr LEFT JOIN [1G_TGS_SERVICIOSYC].[dbo].[vt_usr] t7 WITH (NOLOCK) ON t1.id_emp_lib_apr = t7.id_usr
                LEFT JOIN (SELECT id_req_mat, SUM(total) TotalCosto, COUNT(*) Lineas FROM [1G_TGS_SERVICIOSYC].[dbo].[req_req_mat_det] GROUP BY id_req_mat) t8 ON t1.id_req_mat = t8.id_req_mat    
            WHERE t1.fec_req >= '2023-06-01'
            UNION
            SELECT 'VENTANAS' Empresa, '1G_TGS_VENTANAS' Company, t8.Lineas, t8.TotalCosto, t1.id_req_mat Folio, t1.fec_req FechaRequisicion, t2.nom usuarioSolicita, t3.nom empleadoSolicita, t4.nom dirigidoA, t1.ref Referencia, t5.des Estado, t6.nom empleadoLibero, t1.fec_reg_lib_cot Fecha_liberacion, t7.nom Cotizó, t1.fec_reg_lib_apr, t1.*
            FROM
                [1G_TGS_VENTANAS].[dbo].[req_req_mat] t1 WITH (NOLOCK) LEFT JOIN [1G_TGS_VENTANAS].[dbo].[vt_usr] t2 WITH (NOLOCK) ON t1.id_usr = t2.id_usr	LEFT JOIN [1G_TGS_VENTANAS].[dbo].[vt_usr] t3 ON t1.id_emp_sol = t3.id_emp
                LEFT JOIN [1G_TGS_VENTANAS].[dbo].[vt_usr] t4 WITH (NOLOCK) ON t1.id_emp_dir = t4.id_emp LEFT JOIN [1G_TGS_VENTANAS].[dbo].[vt_status_req] t5 WITH (NOLOCK) ON t1.status = t5.id_status
                LEFT JOIN [1G_TGS_VENTANAS].[dbo].[vt_usr] t6 WITH (NOLOCK) ON t1.id_emp_lib_cot = t6.id_usr LEFT JOIN [1G_TGS_VENTANAS].[dbo].[vt_usr] t7 WITH (NOLOCK) ON t1.id_emp_lib_apr = t7.id_usr
                LEFT JOIN (SELECT id_req_mat, SUM(total) TotalCosto, COUNT(*) Lineas FROM [1G_TGS_VENTANAS].[dbo].[req_req_mat_det] GROUP BY id_req_mat) t8 ON t1.id_req_mat = t8.id_req_mat    
            WHERE t1.fec_req >= '2023-06-01'
            UNION
            SELECT 'ZAID' Empresa, '1G_TGS_ZAID' Company, t8.Lineas, t8.TotalCosto, t1.id_req_mat Folio, t1.fec_req FechaRequisicion, t2.nom usuarioSolicita, t3.nom empleadoSolicita, t4.nom dirigidoA, t1.ref Referencia, t5.des Estado, t6.nom empleadoLibero, t1.fec_reg_lib_cot Fecha_liberacion, t7.nom Cotizó, t1.fec_reg_lib_apr, t1.*
            FROM
                [1G_TGS_ZAID].[dbo].[req_req_mat] t1 WITH (NOLOCK) LEFT JOIN [1G_TGS_ZAID].[dbo].[vt_usr] t2 WITH (NOLOCK) ON t1.id_usr = t2.id_usr	LEFT JOIN [1G_TGS_ZAID].[dbo].[vt_usr] t3 ON t1.id_emp_sol = t3.id_emp
                LEFT JOIN [1G_TGS_ZAID].[dbo].[vt_usr] t4 WITH (NOLOCK) ON t1.id_emp_dir = t4.id_emp LEFT JOIN [1G_TGS_ZAID].[dbo].[vt_status_req] t5 WITH (NOLOCK) ON t1.status = t5.id_status
                LEFT JOIN [1G_TGS_ZAID].[dbo].[vt_usr] t6 WITH (NOLOCK) ON t1.id_emp_lib_cot = t6.id_usr LEFT JOIN [1G_TGS_ZAID].[dbo].[vt_usr] t7 WITH (NOLOCK) ON t1.id_emp_lib_apr = t7.id_usr
                LEFT JOIN (SELECT id_req_mat, SUM(total) TotalCosto, COUNT(*) Lineas FROM [1G_TGS_ZAID].[dbo].[req_req_mat_det] GROUP BY id_req_mat) t8 ON t1.id_req_mat = t8.id_req_mat    
            WHERE t1.fec_req >= '2023-06-01'
            UNION
            SELECT 'EC' Empresa, '1G_TOTALGAS_EC' Company, t8.Lineas, t8.TotalCosto, t1.id_req_mat Folio, t1.fec_req FechaRequisicion, t2.nom usuarioSolicita, t3.nom empleadoSolicita, t4.nom dirigidoA, t1.ref Referencia, t5.des Estado, t6.nom empleadoLibero, t1.fec_reg_lib_cot Fecha_liberacion, t7.nom Cotizó, t1.fec_reg_lib_apr, t1.*
            FROM
                [1G_TOTALGAS_EC].[dbo].[req_req_mat] t1 WITH (NOLOCK) LEFT JOIN [1G_TOTALGAS_EC].[dbo].[vt_usr] t2 WITH (NOLOCK) ON t1.id_usr = t2.id_usr	LEFT JOIN [1G_TOTALGAS_EC].[dbo].[vt_usr] t3 ON t1.id_emp_sol = t3.id_emp
                LEFT JOIN [1G_TOTALGAS_EC].[dbo].[vt_usr] t4 WITH (NOLOCK) ON t1.id_emp_dir = t4.id_emp LEFT JOIN [1G_TOTALGAS_EC].[dbo].[vt_status_req] t5 WITH (NOLOCK) ON t1.status = t5.id_status
                LEFT JOIN [1G_TOTALGAS_EC].[dbo].[vt_usr] t6 WITH (NOLOCK) ON t1.id_emp_lib_cot = t6.id_usr LEFT JOIN [1G_TOTALGAS_EC].[dbo].[vt_usr] t7 WITH (NOLOCK) ON t1.id_emp_lib_apr = t7.id_usr
                LEFT JOIN (SELECT id_req_mat, SUM(total) TotalCosto, COUNT(*) Lineas FROM [1G_TOTALGAS_EC].[dbo].[req_req_mat_det] GROUP BY id_req_mat) t8 ON t1.id_req_mat = t8.id_req_mat    
            WHERE t1.fec_req >= '2023-06-01'
            UNION
            SELECT 'MCP' Empresa, '1G_TOTALGAS_MCP' Company, t8.Lineas, t8.TotalCosto, t1.id_req_mat Folio, t1.fec_req FechaRequisicion, t2.nom usuarioSolicita, t3.nom empleadoSolicita, t4.nom dirigidoA, t1.ref Referencia, t5.des Estado, t6.nom empleadoLibero, t1.fec_reg_lib_cot Fecha_liberacion, t7.nom Cotizó, t1.fec_reg_lib_apr, t1.*
            FROM
                [1G_TOTALGAS_MCP].[dbo].[req_req_mat] t1 WITH (NOLOCK) LEFT JOIN [1G_TOTALGAS_MCP].[dbo].[vt_usr] t2 WITH (NOLOCK) ON t1.id_usr = t2.id_usr	LEFT JOIN [1G_TOTALGAS_MCP].[dbo].[vt_usr] t3 ON t1.id_emp_sol = t3.id_emp
                LEFT JOIN [1G_TOTALGAS_MCP].[dbo].[vt_usr] t4 WITH (NOLOCK) ON t1.id_emp_dir = t4.id_emp LEFT JOIN [1G_TOTALGAS_MCP].[dbo].[vt_status_req] t5 WITH (NOLOCK) ON t1.status = t5.id_status
                LEFT JOIN [1G_TOTALGAS_MCP].[dbo].[vt_usr] t6 WITH (NOLOCK) ON t1.id_emp_lib_cot = t6.id_usr LEFT JOIN [1G_TOTALGAS_MCP].[dbo].[vt_usr] t7 WITH (NOLOCK) ON t1.id_emp_lib_apr = t7.id_usr
                LEFT JOIN (SELECT id_req_mat, SUM(total) TotalCosto, COUNT(*) Lineas FROM [1G_TOTALGAS_MCP].[dbo].[req_req_mat_det] GROUP BY id_req_mat) t8 ON t1.id_req_mat = t8.id_req_mat    
            WHERE t1.fec_req >= '2023-06-01'
            UNION
            SELECT 'TSA' Empresa, '1G_TOTALGAS_TSA' Company, t8.Lineas, t8.TotalCosto, t1.id_req_mat Folio, t1.fec_req FechaRequisicion, t2.nom usuarioSolicita, t3.nom empleadoSolicita, t4.nom dirigidoA, t1.ref Referencia, t5.des Estado, t6.nom empleadoLibero, t1.fec_reg_lib_cot Fecha_liberacion, t7.nom Cotizó, t1.fec_reg_lib_apr, t1.*
            FROM
                [1G_TOTALGAS_TSA].[dbo].[req_req_mat] t1 WITH (NOLOCK) LEFT JOIN [1G_TOTALGAS_TSA].[dbo].[vt_usr] t2 WITH (NOLOCK) ON t1.id_usr = t2.id_usr	LEFT JOIN [1G_TOTALGAS_TSA].[dbo].[vt_usr] t3 ON t1.id_emp_sol = t3.id_emp
                LEFT JOIN [1G_TOTALGAS_TSA].[dbo].[vt_usr] t4 WITH (NOLOCK) ON t1.id_emp_dir = t4.id_emp LEFT JOIN [1G_TOTALGAS_TSA].[dbo].[vt_status_req] t5 WITH (NOLOCK) ON t1.status = t5.id_status
                LEFT JOIN [1G_TOTALGAS_TSA].[dbo].[vt_usr] t6 WITH (NOLOCK) ON t1.id_emp_lib_cot = t6.id_usr LEFT JOIN [1G_TOTALGAS_TSA].[dbo].[vt_usr] t7 WITH (NOLOCK) ON t1.id_emp_lib_apr = t7.id_usr
                LEFT JOIN (SELECT id_req_mat, SUM(total) TotalCosto, COUNT(*) Lineas FROM [1G_TOTALGAS_TSA].[dbo].[req_req_mat_det] GROUP BY id_req_mat) t8 ON t1.id_req_mat = t8.id_req_mat    
            WHERE t1.fec_req >= '2023-06-01'
            UNION
            SELECT 'FG' Empresa, '1G_TGS_FORMULAGAS' Company, t8.Lineas, t8.TotalCosto, t1.id_req_mat Folio, t1.fec_req FechaRequisicion, t2.nom usuarioSolicita, t3.nom empleadoSolicita, t4.nom dirigidoA, t1.ref Referencia, t5.des Estado, t6.nom empleadoLibero, t1.fec_reg_lib_cot Fecha_liberacion, t7.nom Cotizó, t1.fec_reg_lib_apr, t1.*
            FROM
                [1G_TGS_FORMULAGAS].[dbo].[req_req_mat] t1 WITH (NOLOCK) LEFT JOIN [1G_TGS_FORMULAGAS].[dbo].[vt_usr] t2 WITH (NOLOCK) ON t1.id_usr = t2.id_usr	LEFT JOIN [1G_TGS_FORMULAGAS].[dbo].[vt_usr] t3 ON t1.id_emp_sol = t3.id_emp
                LEFT JOIN [1G_TGS_FORMULAGAS].[dbo].[vt_usr] t4 WITH (NOLOCK) ON t1.id_emp_dir = t4.id_emp LEFT JOIN [1G_TGS_FORMULAGAS].[dbo].[vt_status_req] t5 WITH (NOLOCK) ON t1.status = t5.id_status
                LEFT JOIN [1G_TGS_FORMULAGAS].[dbo].[vt_usr] t6 WITH (NOLOCK) ON t1.id_emp_lib_cot = t6.id_usr LEFT JOIN [1G_TGS_FORMULAGAS].[dbo].[vt_usr] t7 WITH (NOLOCK) ON t1.id_emp_lib_apr = t7.id_usr
                LEFT JOIN (SELECT id_req_mat, SUM(total) TotalCosto, COUNT(*) Lineas FROM [1G_TGS_FORMULAGAS].[dbo].[req_req_mat_det] GROUP BY id_req_mat) t8 ON t1.id_req_mat = t8.id_req_mat    
            WHERE t1.fec_req >= '2023-06-01'
            """

        # Ejecutar la consulta y obtener los resultados
        requisitions = ReqReqMat.objects.using('1G_TOTALGAS').raw(sql_query)

        return requisitions