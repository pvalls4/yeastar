How to install the project:

1. Install Python and virtualenv:
    - Visit the Python website (https://www.python.org/) and virtualenv (https://virtualenv.pypa.io/en/latest/installation.html) and download the latest version of both softwares.
    - Run the installer and follow the instructions to install Python on your system.
    - Follow the instructions to install virtualenv through Python commands.

2. Clone the GitHub Repository:
    - Ensure that Git is installed on your system. If not, visit the Git website (https://git-scm.com/) and download the latest version.
    - Open the command prompt or terminal, navigate to the directory where you want to clone the repository.
    - Run the following command to clone the repository: git clone https://github.com/pvalls4/yeastar.git

3. Create a Virtual Environment:
    - Open your command prompt or terminal.
    - Navigate to the directory where you have located this Django project "yeastar".
    - Run the following command to create a virtual environment: python -m virtualenv env

4. Activate the Virtual Environment:
    - On Windows: env\Scripts\activate
    - On macOS/Linux: source myenv/bin/activate

5. Install Project Requirements:
    - Run the following command to install the project requirements: pip install -r requirements.txt

6. Configure the Yeastar settings:
    - Go to the ".env" file and edit your Yeastar's account, password and IP.
    - Please, ensure that your credentials will not be shared. This project already has the .gitignore exception and your file ".env" will not be updated in your git project.

7. Run the Django Development Server:
    - In the command prompt or terminal, ensure that you are still in the project directory.
    - Run the following command to start the Django development server: python maange.py runserver

8. Default Credentials:
    - Django project:
        - Username: admin
        - Password: admin1234
        - Maximum messages per day: 99999
    - Yeastar settings (.env file):
        - Account: yeastar
        - Password: 1234
        - IP: 192.168.5.150

9. Create new accounts:
    - Navigate to Django Admin Pannel ( http://localhost:8000/admin/ )
    - Create a new User with its credentials.

Congratulations! You have successfully set up the Django environment, cloned the project from GitHub, and installed the requirements. The development server should now be running, and you can access your Django project by opening a web browser and navigating to http://localhost:8000/ or the appropriate URL specified in the project.
