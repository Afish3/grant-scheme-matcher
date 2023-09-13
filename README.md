#Scottish Grant Scheme Matcher
--
This is application takes user form data and uses the OpenAI API to match them with grant schemes that they could potentially be eligible for in Scotland.

**Technologies:** 

- OpenAI API
- Langchain
- Flask

		A Note on Scalability: 
		
		Grant data is parsed from individual grant
		scheme PDF documents converted in vector space.
		
		The vectors are stored in a pickle file for easy
		access. To add more grant documents, simply
		delete the pickle file title "all_grants.pkl"
		and re-run the code.


		
	