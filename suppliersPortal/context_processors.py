def companies_processor(request):
    companies = {
        '1G_TGS_AHUMADA': 'Villa Ahumada',
        '1G_TGS_CASTANO': 'Castaño',
        '1G_TGS_CLARA': 'Clara',
        '1G_TGS_GASOMEX': 'Gasomex',
        '1G_TGS_INMO': 'INMO',
        '1G_TGS_JARUDO': 'Jarudo',
        '1G_TGS_PETROTAL': 'Petrotal',
        '1G_TGS_PICACHOS': 'Picachos',
        '1G_TGS_SERVICIOSYC': 'SYC',
        '1G_TGS_VENTANAS': 'VENTANAS',
        '1G_TGS_ZAID': 'ZAID',
        '1G_TOTALGAS': 'Diaz Gas',
        '1G_TOTALGAS_EC': 'EC',
        '1G_TOTALGAS_MCP': '1G_TOTALGAS_MCP',
        '1G_TOTALGAS_TSA': 'TSA',
        '1G_TGS_FORMULAGAS': 'FG',
    }
    return {'companies': companies}
