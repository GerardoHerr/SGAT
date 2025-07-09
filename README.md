# SGAT
Sistema Gestor Académico De Tareas
## Backend (Django)
```bash
//en la carpeta raiz del proyecto
python -m venv env
env/bin/activate
pip install -r requirements.txt

python manage.py runserver

python manage.py makemigrations
python manage.py migrate

cd frontend
npm install
ng serve
