# Python Recipe REST API
#### Software development process: Test-driven development(TDD)

[![Build Status](https://app.travis-ci.com/osakoh/recipe-API.svg?branch=main)](https://app.travis-ci.com/osakoh/recipe-API)

___

#### _Background myth_: A long time ago in a distant land, mankind started discovering different methods of preparing delicious meals :meat_on_bone:. Unfortunately, after a while, people of that land could not enjoy those lovely meals anymore :broken_heart:.  As there were no ways of storing these recipes. This got the people worried :worried:, some became weary :weary:. Oftentimes, people fought themselves :collision: :facepunch:, don't blame them, I mean they were angry :angry:. This posed a serious threat to their taste buds. They then decided to find a solution :wrench: to this problem as this was tearing their community apart. Different scientists were consulted from neighbouring lands.Okay, now this is getting too long :sweat_smile:. 
To be continued........................

---

Back to reality :rocket:.
Recipe REST API is an imaginary box for storing recipes based on their title, ingredients, tag, etc. 

## [Main technologies/Tools required to run this project](requirements.txt)
* Docker
    * Python 3.8
    * Django 3.2
    * Django rest framework 3.12
    * 
* Travis CI
---

## Highlights

- [x] Custom user model 
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

## Different ways to run the test cases within the container
```
python manage.py test app_name.tests
python manage.py test app_name.tests.test_filename
python manage.py test app_name.tests.test_filename.ClassName
python manage.py test app_name.tests.test_filename.ClassName.test_method_name
```



