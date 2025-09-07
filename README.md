Run ```pip install firebase-admin python-dotenv qrcode postmark pandas``` first.

# Example uses

If you want to export all resumes to a csv file, run

```python3 resumes.py```.

If you want to print out every check in link, run

```python3 check_in_links.py```.

# Custom Emails

If you wish to send a custom email out, follow these instructions:
1. First, clone the repo. All your work from here on should either be on an isolated branch, or you should be willing to stash your changes once done and not commit unless extending the email functionality.
2. Decide which email template you will need. For instance, if it's a standard announcement, perhaps it would be best to use the general email template. If it's an email to reset a password which requires the user to press a button, poerhaps it would be best to use the action email template. We'll say you need an action email template for this tutorial.
3. In `json/action.json`, modify the values of the fields so that they match your desired output.
4. Now, if you want to preview what your email will look like, run `python send_emails.py -i workspace/action.json --template action --to <your email here>`. If you'd like to test sending it to multiple emails, run `python send_emails.py -i workspace/action.json --template action --to-list <1st email> <2nd email> ... <nth email>`.
5. If you'd like the email to include the first name of the applicant, add the flag `--first-name` to the command line and any instance of the phrase `{{first_name}}` in the `description` field of the JSON file will be replaced with the first name of the applicant. By default, the first name of the applicant is `there` (so it reads "Hi, there!").
6. When you're ready to send it to real people, decide who you want to send it to. 
    - Send to everyone who was accepted? Use `--to-collection accepted`.
    - Send to everyone who was confirmed? Use `--to-collection confirmed`.
    - Send to everyone? Use `--to-collection all`.
7. Have any other modifications to make? Check out the `emails/base.json` file.
8. Want to make a new template? Add it to `email_templates.py`. For consistency's sake, have a `title` field/argument and a `description` field/argument.

# Updating

If updating this for the new year, check the Firebase website. Log in -> hackharvard-core -> on the left, click the "Build" dropdown -> Firestore database. Then, check the helpers.py header and edit the names of the collections to the appropriate year.

