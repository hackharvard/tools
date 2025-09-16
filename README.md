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

Here's an example email I made:

<img width="556" height="815" alt="image" src="https://github.com/user-attachments/assets/8c6caeae-efb9-494f-a650-325b50fba067" />

## Custom Metadata using CSV

You can use personalized data from a CSV instead of the database. This is useful when you need to send to an arbitrary list or include per-recipient information or values.

Flags involved:
- `--csv_input <CSV>` — load recipients and metadata from a CSV file path
- `--first-name` — enable first-name replacement in `description` (replaces `{{first_name}}` with the first name of the recipient).
        *Note that the csv metadata parser uses str.format (i.e., "{row_name}" instead of "{{row_name}}") and is different in format from the first_name replacement logic.

Example of how personalization works in CSV mode:
- The script replaces `{{first_name}}` in `description` with the `first_name` value or `there` if missing (when `--first-name` is provided).
- It then formats the `description` with all CSV fields using `desc.format(**meta_data)`, so placeholders like `{reimburse_amt}` will be replaced.
- The CSV must include an `email` column. This is enforced and the script will error if missing.
- All `{placeholder}` tokens present in your template `description` must exist as columns in the CSV. If any are missing, the script will stop and list the missing columns.
- If your CSV contains extra columns that are not referenced by the template (excluding `email` and `first_name`), the script will show a one-time warning listing the unused columns and prompt: "Are you sure you want to continue? (y/n)".
 **It is important to name the CSV columns exactly as the placeholders in the description.**




# Updating

If updating this for the new year, check the Firebase website. Log in -> hackharvard-core -> on the left, click the "Build" dropdown -> Firestore database. Then, check the helpers.py header and edit the names of the collections to the appropriate year.

