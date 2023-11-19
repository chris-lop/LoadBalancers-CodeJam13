# LoadBalancers-CodeJam13

https://devpost.com/software/loadbalancers


### Built With
Vue

TailwindCSS

FastAPI

Mapbox GL

Redis

## Getting Started

Prerequisites:
inside of the frontend folder, ```run npm install```
inside of the backend folder, run ```pip install -r requirements.txt```
Install redis and run redis server at address http://localhost:6379

Sign up for a free API key using this link: https://account.mapbox.com/auth/signup/
Have a google maps API with Distance Matrix API enabled

Create a .env file in the backend with the following key:

GOOGLE_API_KEY="YOUR-API-KEY"

Create a .env file in the frontend with the following keys:

VITE_API_SERVER_URL = "YOUR_BACKEND_URL"

VITE_MAP_BOX_GL = "YOUR-API-KEY"

To start the project:

Frontend:

```npm run dev```

Backend:

```uvicorn main:app --reload ```

