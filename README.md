#Scotland Grant Scheme Matcher
--
This application takes user form data and uses the OpenAI API to match them with grant schemes that they could potentially be eligible for in Scotland.

This is designed to increase accessability to grant eligibility criteria that is often not accessible to farmers and other land owners.

## Table of Contents

- [Features](#features)
- [Technologies](#technologies)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
  - [Running the Application](#running-the-application)
  - [Using the Application](#using-the-application)
- [Testing](#testing)

## Features

- Interactive questionnaire to collect user responses.
- Matching user responses with eligibility criteria for various grants.
- Displaying a list of grants that the user may be eligible for.
- Restarting the questionnaire to find new grants.
- Easy-to-use web interface.

## Technologies

- OpenAI API
- Langchain
- Flask

## Getting Started

### Prerequisites

Before beginning, ensure that the following requirements have been met:

- Python 3.11 or higher installed on system.
- PostgreSQL database installed and running (the database configuration can be changed in `app.py`).
- OpenAI API key defined in a `.env` file.

### Installation

Install the necessary requirements in the requirements.txt file

## Usage

### Running-the-application

Once the environment is set-up, run the application to begin.


		A Note on Scalability: 
		
		Grant data is parsed from individual grant
		scheme PDF documents converted in vector space.
		
		The vectors are stored in a pickle file for easy
		access. To add more grant documents, simply
		delete the pickle file title "all_grants.pkl"
		and re-run the code.

### Using-the-application

Once the application is running, the form can be filled out to meet the criteria of a specific user / land owner/manager.

After submitting the form and recieving eligible grants, the form may be started fresh by using the button in the navigation bar.

Grants that a user iis found to be eligible for will be saved in the session for maintaining state and allowing a user to return to the site without having to re-fill out a form.

Potential grant award amounts will be displayed along with links to the appropraite grant application pages.

## Testing
		
Tests for each file are provided and can be run using `$python3 -m unittest test_name`