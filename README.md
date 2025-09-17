Run ```pip install firebase-admin python-dotenv qrcode postmark pandas jinja2``` first.

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
5. When you're ready to send it to real people, decide who you want to send it to. 
    - Send to everyone who was accepted? Use `--to-collection accepted`.
    - Send to everyone who was confirmed? Use `--to-collection confirmed`.
    - Send to everyone? Use `--to-collection all`.
    - Send to everyone on a CSV? Use `--to-csv <path to csv file>`.
        - The CSV file requires at least one column called `email`, `emails`, or `e-mails`.
        - If there are more columns, say, `amount`, you can use the per-recipient value for this column inside of your `.json` input. For instance, your `general.json` file might read:
        ```json
        {
            // ...some other fields here...
            "description" = "Hello, {{(first_name ~ last_name) | title}},",
            "extra_html" = "You have earned a travel reimbursement of <strong>${{amount}}</strong>!"
            // ...some other fields here...
        }
        ```
        This `.json` file would then require your CSV file to have at least an `email` or `emails` column, a `first_name` column, a `last_name` column, and an `amount` column. Notice how we used Jinja2 syntax here to concatenate the first and last name, then piped that output to a title case function. You can use any built in Jinja2 syntax if you'd like.
    > **Note:** When sending emails to real people, be sure to use the `--ignore-exceptions` flag so that any invalid emails don't cause the entire program to crash! 

    > **Note:** You can use `{{first_name}}` at any point in your `.json` input file. By default, it will be replaced as `there` (e.g. "Hello, there!"). If sending to a collection, it will pull the first name from the applicant's profile. If sending to everyone on a CSV file, it will try and pull the first name from a `first_name` column, and if that fails, it will default back to `there`. 
6. Have any other modifications to make? Check out the `emails/base.json` file.
7. Want to make a new template? Add it to `email_templates.py`. For consistency's sake, have a `title` field/argument and a `description` field/argument.

Here's an example email I made:

<img width="556" height="815" alt="image" src="https://github.com/user-attachments/assets/8c6caeae-efb9-494f-a650-325b50fba067" />


# Updating

If updating this for the new year, check the Firebase website. Log in -> hackharvard-core -> on the left, click the "Build" dropdown -> Firestore database. Then, check the helpers.py header and edit the names of the collections to the appropriate year.

