# File Sharing System API

This is a simple File Sharing System API implemented using Django Rest Framework. The API allows users to perform CRUD operations on files, register and login users, and manage user sessions through token-based authentication.

## API Endpoints

1. **Files CRUD Operations**
   - Endpoint: `/api/files/`
   - Methods: GET, POST, PUT, DELETE
   - Description: Allows users to perform CRUD operations on Files model instances.

2. **Get All Files**
   - Endpoint: `/api/all_files/`
   - Method: GET
   - Description: Returns a JSON response containing data for all Files. Requires token-based authentication.

3. **Download File**
   - Endpoint: `/api/download/<int:pk>/`
   - Method: GET
   - Description: Allows downloading a specific file by its primary key. Requires token-based authentication
   
4. **User Registration**
   - Endpoint: `/api/user/register/`
   - Method: POST
   - Description:  Allows user registration with a unique username and email. Returns a JSON response indicating the success or failure of the registration. Additionally, it sends an email verification link to
the registered email address.

5. **Verify Email**
   - Endpoint: `/api/verify-email/<str:verification_token>/`
   - Method: POST
   - Description: Handles email verification. Marks the user's email as verified and clears the verification token.
6. **User Login**
   - Endpoint: `/api/user/login/`
   - Method: POST
   - Description: Allows user login and returns a token upon successful authentication. Returns a JSON response with the token or an error message for invalid credentials.

7. **User Logout**
   - Endpoint: `/api/user/logout/`
   - Method: POST
   - Description: Allows user logout and deletes the authentication token. Requires token-based authentication.

## Model

### Files

- `id` (Auto-generated primary key)
- `pdf` (FileField): Stores the PDF files in the 'store/pdfs/' directory.
  
### UserProfile
- `user` (OneToOneField): Links to the User model.
- `verification_token` (CharField): Stores the unique token for email verification.

