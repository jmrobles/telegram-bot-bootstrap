pybabel extract . -F babel.ini -o locales/base.pot
pybabel update -i locales/base.pot -d locales
