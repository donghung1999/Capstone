# Dong Hung Casting Agency

## Dong Hung Casting Agency Specifications

The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. You are an Executive Producer within the company and are creating a system to simplify and streamline your process.

##### Models:

- Movies with attributes title and release date
- Actors with attributes name, age and gender

##### Endpoints:

- GET /actors and /movies
- DELETE /actors/ and /movies/
- POST /actors and /movies and
- PATCH /actors/ and /movies/

##### Roles:

- Casting Assistant:
  - Can view actors and movies
- Casting Director:
  - All permissions a Casting Assistant has and…
  - Add or delete an actor from the database
  - Modify actors or movies
- Executive Producer
  - All permissions a Casting Director has and…
  - Add or delete a movie from the database

##### Tests:

- One test for success behavior of each endpoint
- One test for error behavior of each endpoint
- At least two tests of RBAC for each role

## Getting Started Project

### Installing (for windows only)

#### Python 3.9

Follow instructions to install 3.9 version of python for your platform in the [python link](https://www.ics.uci.edu/~pattis/common/handouts/pythoneclipsejava/python.html)

#### Installing the requirements package

Navigate to project folder and run commant:

```bash
pip install -r requirements.txt
```

#### Set up for database

To create database, make sure you have right config for `DATABASE_LINK_URL` in setup.sh file and run commant:

```bash
flask db init
flask db migrate
flask db migrate
```

#### Set up to run server

Set environment variable, navigate to project folder and run commant:

```bash
.\setup.sh
set FLASK_APP=app.py
set FLASK_DEBUG=true
flask run --reload
```

### Testing

To deploy the tests, run

```bash
.\setup.sh
python test_app.py
```

### Deploy prject

Project url: [Link](https://donghung-capstone.onrender.com)
Token for each role store in setup.sh file

### Project endpoint

`GET'/movies'`

- Return list of movie with delete status is false from data base
- Request Arguments: None
- Response json:

```json
{
  "success": true,
  "movies": [
    {
      "id": 1,
      "title": "Mui Co Chay",
      "release_date": "Sun, 04 Dec 2022 00:00:00 GMT"
    }
  ]
}
```

`POST'/movies'`

- Create new movie
- Request Arguments: title : string, release_date : Date
- Response json:

```json
{
  "success": true,
  "movies": [
    {
      "id": 1,
      "title": "Mui Co Chay 2",
      "release_date": "Sun, 04 Dec 2022 00:00:00 GMT"
    }
  ]
}
```

`PATCH'/movies'`

- Update movie with given id
- Request Arguments: id : Number, title : string, release_date : Date
- Response json:

```json
{
  "success": true,
  "movies": [
    {
      "id": 1,
      "title": "Mui Co Chay 3",
      "release_date": "Sun, 04 Dec 2022 00:00:00 GMT"
    }
  ]
}
```

`DELETE'/movies'`

- Delete movie with given id
- Request Arguments: id : Number
- Response json:

```json
{
  "success": true,
  "movies": "1"
}
```

`GET'/actors'`

- Return list of actor with delete status is false from data base
- Request Arguments: None
- Response json:

```json
{
  "success": true,
  "actors": [
    {
      "id": 1,
      "name": "Dong Hung",
      "age": 24,
      "gender": "male"
    }
  ]
}
```

`POST'/actors'`

- Create new actor
- Request Arguments: name : string, age : number, gender: string
- Response json:

```json
{
  "success": true,
  "actors": [
    {
      "id": 1,
      "name": "Dong Hung",
      "age": 24,
      "gender": "male"
    }
  ]
}
```

`PATCH'/actors'`

- Update actor with given id
- Request Arguments: id: number, name : string, age : number, gender: string
- Response json:

```json
{
  "success": true,
  "actors": [
    {
      "id": 1,
      "name": "Dong Hung",
      "age": 24,
      "gender": "male"
    }
  ]
}
```

`DELETE'/actors'`

- Delete actor with given id
- Request Arguments: id: number, name : string, age : number, gender: string
- Response json:

```json
{
  "success": true,
  "actors": "1"
}
```
