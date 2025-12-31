# Employee Termination
Application that adds user information to a csv list of termed employees that is periodically processed to perform account disablement actions.
This is a collection of applications and scripts used to process employee terminations.

The main application is setup to be available for use by both IT and HR staff, allowing immetiate terminations to be initiated by HR in instances where IT staff are otherwise occupied or if HR would like to begin the separation process on their own.

The immediate termination and scheduled termination processes are configured to ignore some steps for important accounts such as leadership and IT employees to prevent complications if one of these accounts were accidentally targeted.

# How to Use
To use this application enter the requested fields for the employee that we are separating from; first name, last name, username, their manager's email, the relevant hr employee's email, the users last day, and if the account should be disabled immediately or not.

Some additional notes to be aware of:
* If it is after 3PM CST and the user account should be disabled on the same day you will need to select the following date for the term date and check the box for Immediate termination.
* The users username should be the first 8 characters of their email address, this will come into play if their email address contains more than 8 characters before the @.
  eg. user's email is AIhavealonglastname@dart.net their username would be AIhaveal