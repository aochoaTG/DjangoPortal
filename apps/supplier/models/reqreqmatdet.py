from django.db import models, connections

class ReqReqMatDet(models.Model):
    id_req_mat_det = models.IntegerField(primary_key=True, default=0)
    id_req_mat = models.ForeignKey('ReqReqMat',  # Nombre del modelo relacionado (debe definirse aparte)
        on_delete=models.CASCADE,  # Qué hacer cuando el registro relacionado se borra
        db_column='id_req_mat'  # Nombre exacto del campo en la base de datos
    )
    id_nota = models.IntegerField(default=0)
    id_nota_rech = models.IntegerField(default=0, help_text="En caso de rechazo el Motivo en la nota")
    id_pro = models.IntegerField(default=0)
    id_emp_apr = models.IntegerField(default=0, help_text="Id del empleado que aprobó")
    cant = models.FloatField(default=0)
    costo = models.FloatField(default=0)
    total = models.FloatField(default=0)
    fec_req = models.DateTimeField(default="1900-01-01")
    fec_apr = models.DateTimeField(default="1900-01-01")
    cant_pend = models.FloatField(default=0, help_text="Cantidad Pendiente")
    status = models.PositiveSmallIntegerField(
        default=3,
        help_text="0=Cancelada, 1=Liberada, 2=Concluida, 3=Sin Liberar, 4=Rechazada"
    )
    cant_aprob = models.FloatField(default=0)
    id_nota_desc = models.IntegerField(default=0)
    udm = models.CharField(max_length=5, default="")
    ftr = models.FloatField(default=1)
    id_emp_req = models.IntegerField(default=0)
    id_alm = models.IntegerField(default=0)
    id_impto = models.IntegerField(default=0)
    id_cod_srv = models.IntegerField(default=0)
    id_rel_cot = models.IntegerField(default=0)
    id_usr_apr_rch = models.IntegerField(default=0)
    id_part_oc = models.IntegerField(default=0)
    id_suc_req = models.IntegerField(default=0)
    id_udm = models.IntegerField(default=0)
    id_req_cot = models.IntegerField(default=0)
    id_gto = models.IntegerField(default=0, help_text="ID de la entidad")
    id_cen_cto = models.IntegerField(default=0, help_text="ID del centro de costo")
    id_ref = models.IntegerField(default=0, help_text="ID de la referencia")
    id_prov1 = models.IntegerField(default=0, help_text="ID del proveedor sugerido")
    id_prov2 = models.IntegerField(default=0, help_text="ID2 del proveedor sugerido")
    id_prov3 = models.IntegerField(default=0, help_text="ID del proveedor")
    monto_impto = models.FloatField(default=0)
    totalCImpto = models.FloatField(default=0)
    id_rel_imp = models.IntegerField(default=0)
    id_rel_fac_det = models.IntegerField(default=0)
    id_prov_det = models.IntegerField(default=0)
    c_ind = models.IntegerField(default=0)
    acu_rec = models.FloatField(default=0)
    acu_rec_cxp = models.FloatField(default=0)
    id_com_ser_lot = models.IntegerField(default=0)
    gastos = models.FloatField(default=0)
    gastos_bse = models.FloatField(default=0)
    num_part = models.IntegerField(default=0)
    c_mis_doc = models.PositiveSmallIntegerField(default=0)
    id_bkr = models.IntegerField(default=0)
    id_vig_pre = models.IntegerField(default=0)
    c_apr_auto = models.PositiveSmallIntegerField(default=0)
    descuento = models.FloatField(default=0)
    CtoNeto = models.FloatField(default=0)
    id_cta = models.IntegerField(default=0)
    id_tip_cta = models.IntegerField(default=0)

    class Meta:
        db_table = "req_req_mat_det"
        verbose_name = "Requisición de Material Detalle"
        verbose_name_plural = "Requisiciones de Material Detalle"
        managed = False  # Indica que Django no debe intentar modificar esta tabla

    def get_lines(self, id_req_mat, company):
        sql_query = f"""
        SELECT
            '{company}' Company,
            t1.id_req_mat_det,
            t1.id_req_mat,
            t2.id_emp_sol,
            t2.fec_req FechaRequerida,
            t2.fec_apr FechaAprobada,
            t2.num_doc NoRequisicion,
            t2.fec_doc FechaRequisicion,
            t4.des Concepto,
            LTRIM(RTRIM(ISNULL(t3.nom, '') + ' ' + ISNULL(t3.ap_pat, ''))) EmpleadoSolicita,
            t5.codigo Codigo,
            t5.des Descripcion,
            t19.nota nota_desc,
            t20.nota nota_rechazo,
            t1.udm,
            t1.cant Cantidad,
            t1.cant_aprob CantidadAprobada,
            CONVERT(VARCHAR(50),CONVERT(MONEY,(CASE WHEN t1.status = 1 THEN t6.costo ELSE t1.costo END)),1) AS Costo,
            CONVERT(VARCHAR(50),CONVERT(MONEY,(CASE WHEN t1.status = 1 THEN t6.costo_total ELSE t1.cant * t1.costo END)),1) AS CostoTotal,
            (CASE
                WHEN t1.status = (-1) THEN 'SIN GRABAR'
                WHEN t1.status = 0 THEN 'CANCELADA'
                WHEN t1.status = 1 THEN 'APROBADA'
                WHEN t1.status = 2 THEN 'EN ORDEN'
                WHEN t1.status in (3,99) and t2.c_lib = 0 THEN 'SIN LIBERAR'
                WHEN t1.id_rel_cot >= 0 And t2.c_lib = 1 THEN 'EN COTIZACIÓN'
                WHEN t2.c_lib = 2 THEN 'LIBERADA'
                WHEN t1.status = 4 THEN 'RECHAZADA' END)
            AS Estado,
            t7.codigo CodigoTrabajo,
            t8.des CentroDeCostos,
            CASE WHEN t1.status = 1 THEN 'APROBADA' WHEN t2.c_lib = 2 THEN 'POR APROBAR' ELSE t9.des END EstadoDocumento,
            (SELECT TOP 1 nombre FROM cfg_empresa) Empresa,
            t10.nom_cort AS EmpleadoDirigido,
            REPLACE(LTRIM(RTRIM(t11.rfc)), '-', '') AS rfc_prov1,
            t11.nom1 AS prov1,
            t11.id_mda AS id_mda1,
            t14.codigo prov1_moneda,
            REPLACE(LTRIM(RTRIM(t12.rfc)), '-', '') AS rfc_prov2,
            t12.nom1 AS prov2,
            t12.id_mda AS id_mda2,
            t15.codigo prov2_moneda,
            REPLACE(LTRIM(RTRIM(t13.rfc)), '-', '') AS rfc_prov3,
            t13.nom1 AS prov3,
            t13.id_mda AS id_mda3,
            t16.codigo prov3_moneda,
            num_cta = ISNULL(t17.num_cta, ''),
            cuenta = ISNULL(t17.nom, ''),
            numNomCta = CASE WHEN t1.id_cta = 0 THEN '' ELSE ISNULL(t17.num_cta, '') + ' - ' + ISNULL(t17.nom, '') END,
            t18.usr Aprobador
        FROM
            req_req_mat_det t1
            LEFT JOIN req_req_mat t2 ON t1.id_req_mat = t2.id_req_mat
            LEFT JOIN cat_emp t3 ON t2.id_emp_sol = t3.id_emp
            LEFT JOIN sis_conceptos t4 ON t2.id_cpt = t4.id_cpt
            INNER JOIN cat_pro t5 ON t1.id_pro = t5.id_pro
            LEFT JOIN req_cot t6 ON t1.id_req_cot = t6.id_req_cot
            LEFT JOIN sis_cod_svr t7 ON t1.id_cod_srv = t7.id_cod_svr
            LEFT JOIN ctb_cen_cto t8 ON t1.id_cen_cto = t8.id_cen_cto
            LEFT JOIN vt_status_req t9 ON t2.status = t9.id_status
            INNER JOIN cat_emp t10 ON t2.id_emp_dir = t10.id_emp
            INNER JOIN dbo.cat_prov t11 WITH (nolock) ON t1.id_prov1 = t11.id_prov
            INNER JOIN dbo.cat_prov t12 WITH (nolock) ON t1.id_prov2 = t12.id_prov
            INNER JOIN dbo.cat_prov t13 WITH (nolock) ON t1.id_prov3 = t13.id_prov
            INNER JOIN dbo.mon_monedas AS t14 WITH (nolock) ON t11.id_mda = t14.id_moneda
            INNER JOIN dbo.mon_monedas AS t15 WITH (nolock) ON t12.id_mda = t15.id_moneda
            INNER JOIN dbo.mon_monedas AS t16 WITH (nolock) ON t13.id_mda = t16.id_moneda
            LEFT JOIN dbo.ctb_cta AS t17 WITH (NOLOCK) ON (t17.id_cta = t1.id_cta)
            INNER JOIN dbo.cat_usr t18 WITH (nolock) ON t1.id_usr_apr_rch = t18.id_usr
            INNER JOIN dbo.sis_notas t19 WITH (nolock) ON t1.id_nota_desc = t19.id_nota 
            INNER JOIN dbo.sis_notas t20 WITH (nolock)  ON t20.id_nota = t1.id_nota_rech
        WHERE
            t1.id_req_mat = %s
        """
        # Obtener la conexión a la base de datos 'onegoal'
        with connections[company].cursor() as cursor:
            # Ejecutar la consulta SQL en esa conexión
            cursor.execute(sql_query, [id_req_mat])
            rows = cursor.fetchall()

        # Generar una lista de diccionarios para facilitar el uso en el template
        headers = [
            "Company", "id_req_mat_det", "id_req_mat", "id_emp_sol", "FechaRequerida", "FechaAprobada",
            "NoRequisicion", "FechaRequisicion", "Concepto", "EmpleadoSolicita", "Codigo", "Descripcion",
            "nota_desc", "nota_rechazo", "udm", "Cantidad", "CantidadAprobada", "Costo", "CostoTotal",
            "Estado", "CodigoTrabajo", "CentroDeCostos", "EstadoDocumento", "Empresa", "EmpleadoDirigido",
            "rfc_prov1", "prov1", "id_mda1", "prov1_moneda", "rfc_prov2", "prov2", "id_mda2",
            "prov2_moneda", "rfc_prov3", "prov3", "id_mda3", "prov3_moneda", "num_cta", "cuenta",
            "numNomCta", "Aprobador"
        ]

        data = [dict(zip(headers, row)) for row in rows]

        # Retornar los resultados
        return data

    def get_all_lines(self, from_date=None, until_date=None, company=None):
        # Lista de compañías
        company_ids = [
            '1G_TGS_AHUMADA',
            '1G_TGS_CASTANO',
            '1G_TGS_CLARA',
            '1G_TGS_GASOMEX',
            '1G_TGS_INMO',
            '1G_TGS_JARUDO',
            '1G_TGS_PETROTAL',
            '1G_TGS_PICACHOS',
            '1G_TGS_SERVICIOSYC',
            '1G_TGS_VENTANAS',
            '1G_TGS_ZAID',
            '1G_TOTALGAS',
            '1G_TOTALGAS_EC',
            '1G_TOTALGAS_MCP',
            '1G_TOTALGAS_TSA',
            '1G_TGS_FORMULAGAS'
        ]

        # Si company es diferente de "0", filtramos solo por esa empresa
        if company != "0":
            company_ids = [
                company] if company in company_ids else []

        # Si después del filtro `company_ids` está vacío, no hay empresas válidas
        if not company_ids:
            return []  # Retornar una lista vacía en lugar de ejecutar la consulta

        # Consulta SQL siempre definida
        sql_query = """
                SELECT
                    t1.id_req_mat_det,
                    t1.id_req_mat,
                    t2.id_emp_sol,
                    CONVERT(varchar(10), t2.fec_req, 23) AS FechaRequerida,
                    CONVERT(varchar(10), t2.fec_apr, 23) AS FechaAprobada,
                    t2.num_doc NoRequisicion,
                    CONVERT(varchar(10), t2.fec_doc, 23) AS FechaRequisicion,
                    LOWER(t4.des) Concepto,
                    LOWER(COALESCE(LTRIM(RTRIM(t3.nom)) + ' ' + LTRIM(RTRIM(t3.ap_pat)), '')) AS EmpleadoSolicita,
                    t5.codigo Codigo,
                    LOWER(t5.des) Descripcion,
                    LOWER(CAST(t19.nota AS VARCHAR(MAX))) AS nota_desc,
                    LOWER(CAST(t20.nota AS VARCHAR(MAX))) AS nota_rechazo,
                    t1.udm,
                    t1.cant Cantidad,
                    t1.cant_aprob CantidadAprobada,
                    CAST(
                        CASE 
                            WHEN t1.status = 1 THEN t6.costo 
                            ELSE t1.costo 
                        END AS DECIMAL(18,2)
                    ) AS Costo,
                    CAST(
                        CASE 
                            WHEN t1.status = 1 THEN t6.costo_total 
                            ELSE t1.cant * t1.costo 
                        END AS DECIMAL(18,2)
                    ) AS CostoTotal,
                    (CASE
                        WHEN t1.status = (-1) THEN 'SIN GRABAR'
                        WHEN t1.status = 0 THEN 'CANCELADA'
                        WHEN t1.status = 1 THEN 'APROBADA'
                        WHEN t1.status = 2 THEN 'EN ORDEN'
                        WHEN t1.status in (3,99) and t2.c_lib = 0 THEN 'SIN LIBERAR'
                        WHEN t1.id_rel_cot >= 0 And t2.c_lib = 1 THEN 'EN COTIZACIÓN'
                        WHEN t2.c_lib = 2 THEN 'LIBERADA'
                        WHEN t1.status = 4 THEN 'RECHAZADA' END)
                    AS Estado,
                    t7.codigo CodigoTrabajo,
                    t8.des CentroDeCostos,
                    CASE WHEN t1.status = 1 THEN 'APROBADA' WHEN t2.c_lib = 2 THEN 'POR APROBAR' ELSE t9.des END EstadoDocumento,
                    ce.nombre AS Empresa,
                    LOWER(t10.nom_cort) AS EmpleadoDirigido,
                    REPLACE(TRIM(t11.rfc), '-', '') AS rfc_prov1,
                    t11.nom1 AS prov1,
                    t11.id_mda AS id_mda1,
                    t14.codigo prov1_moneda,
                    REPLACE(TRIM(t12.rfc), '-', '') AS rfc_prov2,
                    t12.nom1 AS prov2,
                    t12.id_mda AS id_mda2,
                    t15.codigo prov2_moneda,
                    REPLACE(TRIM(t13.rfc), '-', '') AS rfc_prov3,
                    t13.nom1 AS prov3,
                    t13.id_mda AS id_mda3,
                    t16.codigo prov3_moneda,
                    num_cta = ISNULL(t17.num_cta, ''),
                    cuenta = ISNULL(t17.nom, ''),
                    numNomCta = CASE WHEN t1.id_cta = 0 THEN '' ELSE ISNULL(t17.num_cta, '') + ' - ' + ISNULL(t17.nom, '') END,
                    t18.usr Aprobador
                FROM
                    req_req_mat_det t1
                    LEFT JOIN req_req_mat t2 ON t1.id_req_mat = t2.id_req_mat
                    LEFT JOIN cat_emp t3 ON t2.id_emp_sol = t3.id_emp
                    LEFT JOIN sis_conceptos t4 ON t2.id_cpt = t4.id_cpt
                    INNER JOIN cat_pro t5 ON t1.id_pro = t5.id_pro
                    LEFT JOIN req_cot t6 ON t1.id_req_cot = t6.id_req_cot
                    LEFT JOIN sis_cod_svr t7 ON t1.id_cod_srv = t7.id_cod_svr
                    LEFT JOIN ctb_cen_cto t8 ON t1.id_cen_cto = t8.id_cen_cto
                    LEFT JOIN vt_status_req t9 ON t2.status = t9.id_status
                    INNER JOIN cat_emp t10 ON t2.id_emp_dir = t10.id_emp
                    INNER JOIN dbo.cat_prov t11 ON t1.id_prov1 = t11.id_prov
                    INNER JOIN dbo.cat_prov t12 ON t1.id_prov2 = t12.id_prov
                    INNER JOIN dbo.cat_prov t13 ON t1.id_prov3 = t13.id_prov
                    INNER JOIN dbo.mon_monedas AS t14 ON t11.id_mda = t14.id_moneda
                    INNER JOIN dbo.mon_monedas AS t15 ON t12.id_mda = t15.id_moneda
                    INNER JOIN dbo.mon_monedas AS t16 ON t13.id_mda = t16.id_moneda
                    LEFT JOIN dbo.ctb_cta AS t17 WITH (NOLOCK) ON (t17.id_cta = t1.id_cta)
                    INNER JOIN dbo.cat_usr t18 ON t1.id_usr_apr_rch = t18.id_usr
                    INNER JOIN dbo.sis_notas t19 ON t1.id_nota_desc = t19.id_nota 
                    INNER JOIN dbo.sis_notas t20 ON t20.id_nota = t1.id_nota_rech
                    CROSS JOIN (SELECT TOP 1 nombre FROM cfg_empresa) ce
                WHERE
                    t2.fec_doc BETWEEN %s AND %s
            """

        all_results = []  # Lista de resultados

        # Iterar sobre cada empresa en company_ids
        for company in company_ids:
            with connections[company].cursor() as cursor:
                cursor.execute(sql_query, [from_date, until_date])
                rows = cursor.fetchall()

                # Definir encabezados de las columnas
                headers = [
                    "Company", "id_req_mat_det", "id_req_mat", "id_emp_sol", "FechaRequerida", "FechaAprobada", "NoRequisicion", "FechaRequisicion", "Concepto", "EmpleadoSolicita", "Codigo", "Descripcion", "nota_desc", "nota_rechazo", "udm", "Cantidad", "CantidadAprobada", "Costo", "CostoTotal", "Estado", "CodigoTrabajo", "CentroDeCostos", "EstadoDocumento", "Empresa",
                    "EmpleadoDirigido", "rfc_prov1", "prov1", "id_mda1", "prov1_moneda", "rfc_prov2", "prov2", "id_mda2", "prov2_moneda", "rfc_prov3", "prov3", "id_mda3", "prov3_moneda", "num_cta", "cuenta", "numNomCta", "Aprobador" ]

                # Convertir los resultados en una lista de diccionarios
                for row in rows:
                    row_dict = dict(zip(headers[1:], row))  # Excluir "Company" del zip
                    row_dict["Company"] = company  # Agregar la compañía

                    # 🎨 Botón Dropdown en HTML
                    row_dict["action"] = f"""
                        <div class="dropdown">
                            <button class="btn btn-primary dropdown-toggle" type="button" data-bs-toggle="dropdown" aria-expanded="false">
                                Acciones
                            </button>
                            <ul class="dropdown-menu">
                                <li><a class="dropdown-item" href="/detalle/{row_dict['id_req_mat_det']}">Ver Detalle</a></li>
                            </ul>
                        </div>
                    """
                    all_results.append(row_dict)  # AQUÍ está el cambio principal - dentro del loop
        return all_results