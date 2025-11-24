En mi proyecto cree un archivo llamado: requirements.txt

flask
gunicorn
mysql-connector-python
python-dotenv


Luego se instalará en EC2 con:

pip install -r requirements.txt

2️⃣
 Clonar el repositorio en EC2
sudo apt update
sudo apt install git -y
git clone https://github.com/TUUSUARIO/TUREPO.git
cd TUREPO


Instalar dependencias del proyecto:

pip install -r requirements.txt

3️⃣
 Instalar MySQL Server en EC2
sudo apt update
sudo apt install mysql-server -y


Iniciar MySQL:

sudo systemctl start mysql

4️⃣
 Crear usuario y base de datos MySQL

Entrar al cliente MySQL:

sudo mysql


Crear base de datos:

CREATE DATABASE cloudcontacts;


Crear usuario MySQL:

CREATE USER 'admin'@'%' IDENTIFIED BY 'GALACTICOVG2025';


Dar permisos:

GRANT ALL PRIVILEGES ON miapp.* TO 'admin'@'%';
FLUSH PRIVILEGES;
EXIT;

5️⃣
 Configurar conexión en .env
DB_HOST=localhost
DB_USER=admin
DB_PASSWORD=TuPasswordSeguro
DB_NAME=miapp

6️⃣
 Ejecutar la aplicación con Gunicorn
gunicorn -b 0.0.0.0:5000 app:app

7️⃣
 Abrir el puerto 5000 en el Security Group

En EC2 > Security Groups > Inbound rules:

Tipo    Puerto    Fuente
Custom TCP    5000    0.0.0.0/0
