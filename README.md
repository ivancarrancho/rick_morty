# Rick & Morty Api

### Steps to reproduce:
  
1. Install python 3.10 
https://www.python.org/downloads/

2. Run: 

```virtualenv rick_morty``` or ```virtualenv --python=/your-python-path/3.10/bin/python3.10 rick_morty```

3. move to *~/rick_morty* folder and run: 

```source bin/activate```

4. Run requirements:

```pip install -r requirements.txt``` or ```pip3.10 install -r requirements.txt```

5. Run the flask app:

```python -m flask run``` or ```python3.10 -m flask run```

## Decode:
should encrypt the **encrypted_email** with MD5:
https://www.md5online.org/md5-encrypt.html
example:

ivan@gmail.com = "d99c9093443e7bfc295ac857adcfa11f"


With the encrypted_email use jwt, Python example:

**encoded_jwt** should be the api response: 

    import jwt
    jwt.decode(encoded_jwt, encrypted_emai, algorithms=["HS256"])
    
    jwt.decode(
        encoded_jwt, 
        "d99c9093443e7bfc295ac857adcfa11f", 
        algorithms=["HS256"]
    )

## Postman collection
https://www.getpostman.com/collections/5f9dc62878c68348009d
