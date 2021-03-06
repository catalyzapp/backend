# Catalyz (Backend)
Catalyz is a service that matches people with similar challenges and circumstances

## Backend API
The backend JSON API has the following endpoints:

* `/user` - Represents a user resource
  * `POST /`
    * Creates a new user
    * Input:
        * facebook_id :: string
        * first_name :; string
        * last_name :: string
        * email :: string
        * image_link :: string
        * language :: string
        * country_of_origin :: string
        * gender :: string
        * bio :: string
        * interest :: string
        * role :: string{mentor, mentee}    
    * Output
        * If successfully created, {status 200}
        * If failure, {status 400}
  * `GET /<facebook_id:string>`
    * Obtains information about a user
    * Output
        * If user exists, {status 200}
            * facebook_id :: string
            * first_name :: string
            * last_name :: string
            * email :: string
            * image_link :: string
            * language :: string
            * country_of_origin :: string
            * gender :: string
            * bio :: string
            * interest :: string
            * role :: string{mentor, mentee}
        * If user doesn't exist, {status 400}
        
* `/matchup` - Represents a call to find the best possible match between mentor and mentee
    * `POST /`
        * Matches a mentee to a mentor
        * Input
            * facebook_id :: string{facebook_id}
        * Output
            * recommendations :: [{mentor, mentor_bio, mentee, mentee_bio, similarity_score}]
        
* `/conversation` - Represents a conversation instance between a mentor and mentee
    * `POST /`
        * Gets a specific conversation's stream of messages in chronological order
        * Input
            * mentor :: string{facebook_id}
            * mentee :: string{facebook_id}
        * Output:
            * mentor :: string
            * mentee :: string
            * timestamp :: string
            * messages :: {sent_by :: string{facebook_id}, message :: string, timestamp :: string}
            
* `/history` - Represents a history of conversations a user has had
    * `POST /`
        * Gets a list of all conversations a user has had
        * Input
            * facebook_id :: string{facebook_id}
         * Output[]:
            * mentor :: string
            * mentor_bio :: string
            * mentee :: string
            * mentee_bio :: string
            * timestamp :: string

* `/message` - Represents an atomic message within a conversation
  * `POST /`
    * Creates a new message
    * Input:
        * mentor :: string{facebook_id}
        * mentee :: string{facebook_id}
        * sent_by :: string{facebook_id}
        * message :: string
        * timestamp :: string

## Database Schema
* **user** (primary key: facebook_id)
    * facebook_id :: string
    * first_name :: string
    * last_name :: string
    * email :: string
    * image_link :: string
    * language :: string
    * country_of_origin :: string
    * gender :: string
    * bio :: string
    * interest :: string
    * role :: string{mentor, mentee}
* **conversation** (primary key: id)
    * id :: int
    * mentor :: user.facebook_id
    * mentee :: user.facebook_id
    * timestamp :: timestamp(with time zone)
* **message** (primary key: conversation_id, sent_by, timestamp)
    * conversation_id :: conversation.id
    * sent_by :: user.facebook_id
    * message :: string
    * timestamp :: timestamp(with time zone)
    