This file will discuss in briefly about the major classes and functions we have used to built our software.

## forms.py:

### Class UserFormAdmin and UserFormStudent
These classes are used to capture the basic data like firstname, lastname, email and password of Admin and student respectively.

### Class ComplainForm
This class is used to capture details of a new complain.

### Class LoginForm
This class is used to capture the username and password every time someone tries to login into our system.

### Class ChangeStatusForm
This class is used to update the status of a complain to one of the following - Pending, Viewed, Solved and Rejected.

### Class AdminProfileForm and StudentProfileForm
This class is used to capture the college name and branch of the associated user.

### Class EditAdmin and EditStudent 
This class is used to update the college name, branch and designation of Admin and college name and branch of student.

### CLass EditUser
This is used to update the firstname, lastname, email and username of a particular user.


## decorators.py:

### Method is_logged
This method checks whether the user is Student or a faculty member.

### Method admin_required and student_required
This method checks the user category and shows the appropriate view and if user is of other category then shows an error.

### Method adminprofile_required and studentprofile_required
This method checks the user category and redirects them to their profile page. 

## models.py
This file contains the various models which are required for database integration.

### Class Admin
This class is triggered to select the college, Department and designation of Admin.

### CLass Student 
This class is triggered to select the college and branch of Student.

### Complain
This class is triggered to select the various attributes of Complain.

