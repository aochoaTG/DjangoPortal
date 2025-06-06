# common/utils.py

def get_user_info(user):
    """Devuelve un diccionario con los campos del usuario, sus grupos y permisos."""
    if not user.is_authenticated:
        return {'error': 'Usuario no autenticado'}

    user_data = {
        field.name: getattr(user, field.name)
        for field in user._meta.fields
    }

    # Agrega grupos
    user_data['groups'] = list(user.groups.values_list('name', flat=True))

    # Agrega permisos (como strings legibles)
    user_data['permissions'] = list(user.get_all_permissions())

    return user_data
