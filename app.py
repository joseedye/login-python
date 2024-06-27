from flask import Flask, render_template,request, jsonify
import win32security
import win32api
import win32netcon
import win32api
import win32net

app = Flask(__name__)

@app.route('/')

def index():
    return render_template('index.html')


# Ruta para autenticar usuario de Windows
@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    try:
        # Validar las credenciales del usuario contra Windows
        varia = win32security.LogonUser(
            username,
            None,
            password,
            win32security.LOGON32_LOGON_NETWORK,
            win32security.LOGON32_PROVIDER_DEFAULT
        )
        print('adios')
        print(varia)
        print(f"Handle: {varia}")
        print(f"Tipo de handle: {type(varia)}")
        print('adios2')

        # Ejemplo de uso
        username = "joseeduardo"
        domain = None  # Puedes especificar el dominio si no es local
        print(username)



        # Obtener roles del usuario
        roles = obtener_roles_de_usuario(username, None)
        print(roles)

        if roles:
            print(f"Roles del usuario '{username}':")
            for role in roles:
                print(f"- {role}")
        else:
            print(f"No se encontraron roles para el usuario '{username}'")




        # Si la autenticación es exitosa, devuelve un mensaje de éxito
        # obtener_grupos_de_usuario(username,None)
        return jsonify({'message': 'Autenticación exitosa para {}'.format(username)})
    except Exception as e:
        # Si hay un error durante la autenticación, devuelve un mensaje de error
        return jsonify({'error': str(e)}), 401




    # return '¡Hola, mundo! Esta es mi primera aplicación Flask.'


def obtener_grupos_de_usuario(username, domain=None):
    print('emtro en obtener grupos de usuario')
    groups = []
    resume_handle = 0
    
    try:
        while True:
            # Obtener lista de grupos de usuario
            user_info = win32net.NetUserGetLocalGroups(domain, username, 0)
            # user_info = win32net.NetUserGetLocalGroups(domain, username, 0, resume_handle, win32netcon.MAX_PREFERRED_LENGTH)

            for group in user_info:
                groups.append(group['name'])
                print(group['name'])

            if not resume_handle:
                break

    except win32net.error as e:
        print(f"Error al obtener grupos de usuario: {e}")

    return groups

def obtener_grupos_de_usuario(username, servername=None):
    groups = []
    resume_handle = 0

    try:
        while True:
            user_info = win32net.NetUserGetLocalGroups(servername, username, 0)

            for group in user_info:
                groups.append(group['name'])

            if not resume_handle:
                break

    except win32net.error as e:
        print(f"Error al obtener grupos de usuario: {e}")

    return groups



def obtener_roles_de_usuario(username, servername=None):
    roles = []
    print(f'enntro en la funcion {username}')
    try:
        groups = obtener_grupos_de_usuario(username, servername)
        print('grupos')
        print(groups)
        # Definir roles conocidos o grupos de interés
        roles_conocidos = {
            "Administradores": "Administradores",
            "Usuarios con acceso de red": "Usuarios",
            # Puedes agregar más roles según tu entorno
        }
        
        # Buscar roles conocidos en los grupos del usuario
        for role, group_name in roles_conocidos.items():
            if group_name in groups:
                roles.append(role)
    
    except Exception as e:
        print(f"Error al obtener roles de usuario: {e}")
    
    return roles



if __name__ == '__main__':
    app.run(debug=True)  
