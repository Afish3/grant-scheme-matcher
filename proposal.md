#**Project Proposal:**
<hr>

* **Problem**: 

	There is a lack of accessibility for local farmers in Scotland to learn about and apply for appropriate grants that will give money for land and habitat management. Without putting in extensive amounts of time and energy into researching available grants, many are unable to get the money that the grants provide to encourage the management of woodlands by planting trees, and encouraging biodiversity in the woodlands.

* **Solution**: 

	This website will act as a bridge between the confusing world of grants and the requirements that go into being eligible for them, and the local farmer / resident who can use the grant money to promote woodland preservation and biodiversity all throughout the country.

* **Data**: 

	I plan to use data from the list of available grants from the Forestry Grant Scheme as well as user input coming from a form submission that will match each project to appropriate and applicable grants. This will also make it clear to users how much money they are able to receive from the grant based on their input.

* **Database**: 

		Files will be stored locally?

	User login data will be stored in a single database for authentication and saving projects/grants to their own dashboard.

* **API**:

	I will use AI tools including langchain, OpenAI or HuggingFace to analyze form data and find relevant grants.

	Problems I may run into are accuracy and speed.

* **Security**: 

	Passwords for users will be hashed using bcrypt and stored safely. Additionally API keys and other secret keys will be included as environment variables when deployed.

* **Functionality**:

	I would like to see this application have the functionality to find appropriate grants based on form submissions.

	The option to create an account and save the project and grant to a user dashboard that would...
	
	```
	connect the files stored locally to the 
	users id in the database?
	```

	I would like the grants and user’s form data to save in the session if they are not logged in to increase accessibility.
