## Oliver Cole 10859527

# COMP2001---TrailService

My microservice is designed to manage trails, location points, and tags for a well-being trail application. It has CRUD operations for trails, location points, and tags and has role-based access control.

## Features

- **Trail CRUD Operations**: Manage trail data.
- **Location Points Management**: Add and retrieve location points for a trail.
- **Tagging System**: Add tags to trails.
- **Authentication**: Secure login/logout using the external authentication API.
- **Role-Based Access Control**: Admin users have full access, while regular users and non-logged-in users have limited access.
- **Swagger UI Documentation**: The API is documented with Swagger, accessible via a browser.


## API Overview

- **Authentication**  
  `POST /login` – User login  
  `POST /logout` – User logout

- **Trails**  
  `GET /trails` – Retrieve all trails  
  `GET /trails/{trail_id}` – Retrieve a trail by ID  
  `POST /trails` – Create a new trail (Admin only)  
  `PUT /trails/{trail_id}` – Update a trail by ID (Admin only)  
  `DELETE /trails/{trail_id}` – Delete a trail by ID (Admin only)  

- **Location Points**  
  `GET /location_points` – Retrieve all location points  
  `POST /location_points` – Add a new location point (Admin only)  
  `PUT /location_points/{location_point_id}` – Update a location point by ID (Admin only)  
  `DELETE /location_points/{location_point_id}` – Delete a location point by ID (Admin only)  

- **Tags**  
  `GET /tags` – Retrieve all tags  
  `POST /tags` – Add a new tag (Admin only)  
  `PUT /tags/{tag_id}` – Update a tag by ID (Admin only)  
  `DELETE /tags/{tag_id}` – Delete a tag by ID (Admin only)  

---

## Running with Docker

1. **Build the Docker Image**  
   ```bash
   docker build -t trailservice:latest .
   ```

2. **Run the Docker Container**  
   ```bash
   docker run -d -p 8000:8000 trailservice:latest
   ```

Access the API at [http://localhost:8000/api/ui](http://localhost:8000/api/ui).
