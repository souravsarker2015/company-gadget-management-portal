# Company Device Management Portal

<div id="top"></div>
<div align="center">

  <p align="center">
    The "Company Device Management Portal" is a Software as a Service (SAAS) application designed to serve multiple companies within a single platform. This application facilitates comprehensive device tracking for each company, allowing for the management of assigned devices, tracking of assignment and return times, monitoring device conditions, and providing other essential tracking solutions. The platform ensures efficient and organized management of company devices, enhancing overall operational control and accountability.
    <br />
    
  </p>
</div>

### Built With
* [Python](https://Python.org/)
* [Django](https://www.djangoproject.com/)
* [Django Rest Framework](https://www.django-rest-framework.org/)
* [mysql](https://www.mysql.com/)



## Task Accomplished
* Firstly, I created my virtual environment and configured the MySQL database for my project. I also created a Django app named "company_device_management_portal."
* Next, I developed all the necessary models and serializers in different app directories.
* Subsequently, I created various classes in the view files of each app, as required.
* To ensure a modular and well-organized structure, I employed the factory design pattern to retrieve necessary data or queries. Business logics are not directly implemented in the view files; instead, I created separate use_cases files to handle business logic and queries.
* I integrated Swagger documentation to facilitate the testing of all APIs. Additionally, I conducted thorough testing using Postman.
* I have included the company_id in the header, and it is also documented in Swagger because of its integral role in the interconnected structure of everything related to the company. Testing the APIs does not require any user access token or credentials.
* Following successful testing, I implemented test cases in the test files of all the apps.
* I updated all the admins.py files to reflect the changes.
* I've implemented custom login, registration, and logout functionalities. Consequently, in the views, obtaining the company_id can be done using request.user.company.id when the IsAuthenticated permissions class is present. In such cases, there's no need to explicitly pass the company_id in the request header. This approach ensures a fully authenticated SAAS application. For the betterment of testing, I have intentionally omitted the permission class

### Prerequisites
You have to Install those things to run the Project 
* python (I have used python3.9)
  ```sh
  install python in your os
  ```

* Django
  ```sh
  pip install django
  ```
* Django Rest Framework
  ```sh
  pip install djangorestframework
  ```
* mysqlclient
  ```sh
  pip install mysqlclient
  ```

### Installation
You should check requirements.txt from the project repository
<br>  
1. Clone the repo
   ```sh
   git clone https://github.com/souravsarker2015/company_device_management_portal

   ```

2. Install Python(I have used python3.9)
   ```sh
   install Python in your os
   ```
3. Create a virtual env as venv or as you wish
   ```sh
   python3.9 -m venv venv or your virtual environment name 
   ```
4. I have configured the settings for a MySQL database, but you can also use an SQLite database. The configuration details are specified in the local.py file within the settings directory.
   
5. Create a .env file in the root directory with necessary data 
   ```sh
    DEBUG=True
    DATABASE_USER=''
    DATABASE_PASSWORD=''
    DATABASE_NAME=""
    SECRET_KEY=""
    OAUTH2_PROVIDER_CLIENT_ID=''
    OAUTH2_PROVIDER_CLIENT_SECRET=''
    CUSTOM_AUTH_BACKEND_URL=http://localhost:8000/ or your project port
   ```
6.  one can easily create OAUTH2_PROVIDER_CLIENT_ID and OAUTH2_PROVIDER_CLIENT_SECRET using the django-oauth-toolkit. client id and client secret is necessary for login registration.'http://localhost:8000/o/applications/register/' one can create client id and client secret.Need to select Client type=Confidential, Authorization grant type= Resource owner password-based.

7. Install Necessary Packages 
   ```sh
   pip install -r requirements/base.txt
   ```


## Project Link
Project Link: [https://github.com/souravsarker2015/company_device_management_portal](https://github.com/souravsarker2015/company_device_management_portal)

## Contact

Your Name: Sourov Sarker
<br />
Email: [souravsarker2015@gmail.com](https://mail.google.com/mail/u/0/)
<br>
LinkedIn: [https://www.linkedin.com/in/souravsarker2015/](https://www.linkedin.com/in/souravsarker2015/)
<br>










