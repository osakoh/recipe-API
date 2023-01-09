# Python Recipe REST API
#### Software development process: Test-driven development(TDD)

![Build Status](https://github.com/osakoh/recipe-API/actions/workflows/checks.yml/badge.svg)

Recipe REST API is an imaginary box for storing recipes based on their title, ingredients, tag, etc. 

## [Main technologies/Tools required to run this project](requirements/base.txt)
* Docker
    * Python 3.9
    * Django 3.2
    * Django rest framework 3.12
    * PostGreSQL
* GitHub Actions
---

## Highlights

- [x] Fix for DB race condition
- [x] Custom user model 
- [x] API documentation using [drf-spectacular](https://drf-spectacular.readthedocs.io/en/latest/)
- [x] Swagger and OpenAPI Schema
- [x] Sorting
- [x] Filtering
- [x] Image uploading
- [x] Robust test cases

## Commands
- Running the container without specifying a filename
```
docker-compose up 
```
- Running the container specifying filename

```
docker-compose -f docker-compose-local.yml up
```

- View running container(s)
```
docker ps
```

- Execute commands in the container
```
docker exec -it <container-id> sh
```

### Different ways to run test cases within the container
```
python manage.py test
python manage.py test app_name
python manage.py test app_name.tests.test_filename
python manage.py test app_name.tests.test_filename.ClassName
python manage.py test app_name.tests.test_filename.ClassName.test_method_name
```



