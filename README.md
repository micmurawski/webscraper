### Zadanie

uruchomienie

```buildoutcfg
docker-compose build
docker-compose up
```

### Dokumentacja API

http://127.0.0.1:8000/api/v1/docs/


### Parametry Środowiskowe
Żeby uruchomić upload plików do S3 koniecznie jest podanie kluczy API w zmiennych środowiskowych backendu w pliku docker-compose.yml
````
AWS_ACCESS_KEY: ...
AWS_SECRET_KEY: ...
BASE_URL: ...
S3_REGION_NAME: ...
```
