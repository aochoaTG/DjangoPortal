from django.db import connection, connections
from django.http import \
    JsonResponse, \
    HttpResponse


def get_purchase_orders(request, company, from_date, until_date):
    query = f"""
    SELECT DISTINCT
        '{company}' AS company,
        (SELECT raz_soc FROM cfg_empresa) AS raz_soc,
        oc.id_req_mat AS Requisicion,
        oc.Estatus,
        oc.num_doc AS [Orden Compra],
        oc.fec_doc AS [Fecha OC],
        oc.Proveedor AS [Proveedor],
        ISNULL(CONVERT(MONEY, oc.Importe), 0) AS [SubTotal],
        ISNULL(CONVERT(MONEY, oc.Imptos), 0) AS [Imptos.],
        ISNULL(CONVERT(MONEY, oc.Total), 0) AS [Total],
        CASE 
            WHEN oc.status IS NOT NULL THEN 'SI' 
            ELSE 'NO' 
        END AS [CXP Registrada],
        ISNULL(oc.no_fact, '') AS [Factura],
        CASE ISNULL(oc.status, 0)
            WHEN 0 THEN ''
            WHEN 2 THEN 'PAGADA'
            ELSE 'NO PAGADA'
        END AS [Estatus Factura]
    FROM req_req_mat r WITH (NOLOCK)
    LEFT JOIN (
        SELECT
            part.id_req AS id_req_mat,
            enc.num_doc,
            enc.fec_doc,
            enc.fec_reg,
            SUM(part.importe) AS Importe,
            SUM(part.imptos) AS Imptos,
            SUM(part.total) AS Total,
            sta.[des] AS Estatus,
            p.nom1 AS Proveedor,
            cxp.no_fact,
            cxp.status
        FROM dbo.com_mov_doc AS enc WITH (NOLOCK)
        JOIN dbo.com_mov_part AS part WITH (NOLOCK) ON part.id_compra = enc.id_compra
        JOIN dbo.cat_estatus AS sta WITH (NOLOCK) ON sta.tipo = 2 AND sta.id_status = enc.[status]
        JOIN req_req_mat_det AS rd WITH (NOLOCK) ON rd.id_req_mat_det = part.id_part_req
        JOIN cat_prov AS p WITH (NOLOCK) ON p.id_prov = enc.id_prov
        LEFT JOIN (
            SELECT  
                id_part_orig, id_compra, status, c.no_fact
            FROM cxp_doc_det d WITH (NOLOCK)
            INNER JOIN cxp_doc c WITH (NOLOCK) ON d.id_cxp_doc = c.id_cxp_doc
            WHERE status <> 3
        ) cxp ON cxp.id_part_orig = part.id_part AND cxp.id_compra = part.id_compra
        WHERE enc.id_tip_doc = 86 AND enc.status <> 3 AND ISNULL(cxp.status, 1) <> 3
        GROUP BY 
            part.id_req, enc.num_doc, enc.fec_doc, enc.fec_reg, sta.[des], p.nom1, cxp.no_fact, cxp.status
    ) oc ON oc.id_req_mat = r.id_req_mat
    WHERE oc.num_doc IS NOT NULL AND oc.fec_doc BETWEEN '{from_date}' AND '{until_date}'
    ORDER BY oc.num_doc DESC;
    """

    with connections[company].cursor() as cursor:
        cursor.execute(query, [])
        columns = [col[0] for col in cursor.description] # Obtener los nombres de las columnas
        results = []
        for row in cursor.fetchall(): # Recorrer cada fila
            row_dict = dict(zip(columns, row)) # Convertir la fila en un diccionario
            for key, value in row_dict.items(): # Convertir valores de tipo bytes a str
                if isinstance(value, bytes): # Si el valor es de tipo bytes
                    row_dict[key] = value.decode('utf-8') # Convertir a str
            results.append(row_dict) # Agregar el diccionario a la lista de resultados

    return results  # Retornamos la lista de resultados

def get_company_data(request, company):
    query = f"SELECT *, LOWER(Calle) AS CalleLower, LOWER(Colonia) as ColoniaLower, LOWER(Ciudad) as CiudadLower, LOWER(Estado) as EstadoLower FROM [1G_TOTALGAS].[dbo].[cfg_empresa]"
    with connections[company].cursor() as cursor:
        cursor.execute(query, [])
        columns = [col[0] for col in cursor.description] # Obtener los nombres de las columnas
        results = []
        for row in cursor.fetchall(): # Recorrer cada fila
            row_dict = dict(zip(columns, row)) # Convertir la fila en un diccionario
            for key, value in row_dict.items(): # Convertir valores de tipo bytes a str
                row_dict[key] = str(value) # Convertir a str
            results.append(row_dict) # Agregar el diccionario a la lista de resultados

    return results  # Retornamos la lista de resultados