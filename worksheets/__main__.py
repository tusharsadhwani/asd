"""
Script to read Codenscious' daily worksheets
and generate Project-wise daily worksheets
"""

# pylint: disable=no-member
import os.path
import pickle
import datetime
import dateutil.parser

import utils

WORKSHEETS_FOLDER_ID = '1TDm900uOcwFLluness6Zo0m7gi0ax2aq'
GENERATED_WORKSHEETS_FOLDER_ID = '1KT2iJwht33XxpI2UE0f5dH005z-yC9uD'

PARSERINFO = dateutil.parser.parserinfo(dayfirst=True)

CURRENT_YEAR = datetime.datetime.now().year
CURRENT_MONTH = datetime.datetime.now().month
CURRENT_MONTH_NAME = datetime.datetime.now().strftime('%B').upper()

CURRENT_YEAR = 2019
CURRENT_MONTH = 6
CURRENT_MONTH_NAME = 'JUNE'


def load_user_folders(drive_api, folder_id):
    "Loads the user folders inside the worksheet folder"
    user_results = drive_api.files().list(
        q=f"""
            mimeType='application/vnd.google-apps.folder' and
            '{folder_id}' in parents and
            trashed=False
        """,
        fields="files(id, name, parents)").execute()

    items = user_results.get('files', [])

    for item in items:
        assert folder_id in item['parents']

    user_ids = {item['name']: item['id'] for item in items}
    return user_ids


def load_user_spreadsheets(drive_api, user_ids):
    "Loads all of this month's spreadsheets from user folders"
    user_spreadsheets_dict = {}
    for user_name, user_folder_id in user_ids.items():
        user_spreadsheets = {}
        spreadsheet_results = drive_api.files().list(
            q=f"""
                mimeType='application/vnd.google-apps.spreadsheet' and
                '{user_folder_id}' in parents and
                trashed=False
            """,
            fields="files(id, name, parents)").execute()

        spreadsheets = spreadsheet_results.get('files', [])
        for spreadsheet in spreadsheets:
            if (CURRENT_MONTH_NAME in spreadsheet['name'].upper() and
                    str(CURRENT_YEAR) in spreadsheet['name']):

                user_spreadsheets[spreadsheet['name']] = spreadsheet['id']
        user_spreadsheets_dict[user_name] = user_spreadsheets

        print(f"User {user_name} loaded")

    return user_spreadsheets_dict


def import_spreadsheets(sheets_api, users_dict):
    "Imports all spreadsheets by month into a dictionary"
    spreadsheets_data = {}
    for user_name, spreadsheets_dict in users_dict.items():
        for spreadsheet_name, spreadsheet_id in spreadsheets_dict.items():
            if spreadsheet_name.lower() not in spreadsheets_data:
                spreadsheets_data[spreadsheet_name.lower()] = {}
            if user_name not in spreadsheets_data[spreadsheet_name.lower()]:
                spreadsheets_data[spreadsheet_name.lower()][user_name] = {
                    'body': []}

            result_body = (sheets_api
                           .spreadsheets()
                           .values()
                           .get(spreadsheetId=spreadsheet_id, range='A:I')
                           .execute())

            sheet_data = result_body.get('values', [])
            spreadsheets_data[spreadsheet_name.lower(
            )][user_name]['body'] += sheet_data

            print(f"Imported {user_name.strip()}/{spreadsheet_name}")

    return spreadsheets_data


def get_project_ids(spreadsheets_data):
    "Gets a list of all project IDs used in the worksheets"
    project_ids = set()
    for spreadsheet in spreadsheets_data.values():
        for user_data in spreadsheet.values():
            for row in user_data.get('body', []):
                if len(row) > 8:
                    project_ids_in_cell = [pid.strip()
                                           for pid in row[8].split(',')]
                    for project_id in project_ids_in_cell:
                        project_id = project_id.strip().upper()
                        if (project_id
                                and project_id not in project_ids
                                and project_id != 'PROJECT ID'):
                            project_ids.add(project_id)
                            print(f"Project Name {project_id} added")
    return project_ids


def confirm_project_names(project_ids):
    """
    Compares project IDs to saved project names, verifies
    unknown project names, and shows the rows of data that
    contain incorrect project IDs.
    """
    projects_dict = None
    invalid_project_ids = []

    if os.path.exists('projectnames.pickle'):
        with open('projectnames.pickle', 'rb') as projects_file:
            projects_dict = pickle.load(projects_file)

    if projects_dict is None:
        projects_dict = {}

    for project_id in project_ids:
        if project_id not in projects_dict:
            print()
            print('-'*30)
            valid_input = input(f"Is {project_id} a valid project? Y/N: ")
            valid = valid_input.strip().lower() == 'y'

            if valid:
                project_name = input("Enter name of the project: ").strip()
                print(f"{project_id} - {project_name}")
                confirm = input("Confirm? Y/N: ").strip().lower() == 'y'

                if confirm:
                    projects_dict[project_id] = project_name
                    print(f"Project {project_name} added.")
                else:
                    invalid_project_ids.append(project_id)
                    print("Ok.")
            else:
                invalid_project_ids.append(project_id)
                print("Ok.")

    with open('projectnames.pickle', 'wb') as projects_file:
        pickle.dump(projects_dict, projects_file)

    return projects_dict, invalid_project_ids


def print_rows_with_invalid_ids(spreadsheets_data, invalid_project_ids):
    "Prints rows with invalid Project IDs"
    bad_rows = []
    for spreadsheet in spreadsheets_data.values():
        for user_data in spreadsheet.values():
            for row in user_data.get('body', []):
                if len(row) >= 9:
                    project_ids_in_cell = [pid.strip().upper()
                                           for pid in row[8].split(',')]
                    for project_id in project_ids_in_cell:
                        if project_id in invalid_project_ids:
                            bad_rows.append(row)

    if bad_rows:
        print()
        print("ROWS WITH UNKNOWN PROJECT IDS:")
        for bad_row in bad_rows:
            print(bad_row)
        exit()


def format_spreadsheets(spreadsheets_data, projects_dict):
    "Formats the spreadheet data into separate projects"
    bad_rows = []
    for spreadsheet in spreadsheets_data.values():
        for user_data in spreadsheet.values():
            for row in user_data.get('body', []):
                date = row[0] if row else ''
                try:
                    parsed_date = dateutil.parser.parse(
                        date, parserinfo=PARSERINFO)
                    if (parsed_date.month == CURRENT_MONTH and
                            parsed_date.year == CURRENT_YEAR):
                        row[0] = [parsed_date.year,
                                  parsed_date.month, parsed_date.day]
                    else:
                        bad_rows.append(row)
                except ValueError:
                    if row and row[0].strip().upper() not in ['DAY', 'DATE']:
                        bad_rows.append(row)

    if bad_rows:
        print("THE FOLLOWING ROWS ARE BAD:")
        for bad_row in bad_rows:
            print(bad_row)
        exit()

    projects_data = {}
    for spreadsheet in spreadsheets_data.values():
        for user_name, user_data in spreadsheet.items():
            for row in user_data.get('body', []):
                if len(row) > 8:
                    date_list = row[0]
                    date = f"{date_list[2]}/{date_list[1]}/{date_list[0]}"

                    project_ids_in_cell = [pid.strip().upper()
                                           for pid in row[8].split(',')]
                    for project_id in project_ids_in_cell:
                        if project_id == 'PROJECT ID':
                            continue

                        assert project_id in projects_dict

                        if project_id not in projects_data:
                            projects_data[project_id] = {}
                        if date not in projects_data[project_id]:
                            projects_data[project_id][date] = {}
                        if user_name not in projects_data[project_id][date]:
                            projects_data[project_id][date][user_name] = []

                        projects_data[project_id][date][user_name].append(
                            row[1:])

    for projects in projects_data.values():
        for dates_data in projects.values():
            for sheet_body in dates_data.values():
                sheet_body.sort(key=lambda l: l[0])

    current_projects = {pid: pname
                        for (pid, pname) in projects_dict.items()
                        if pid in projects_data}

    return projects_data, current_projects


def generate_spreadsheets(drive_api, sheets_api, spreadsheets_data, projects_dict):
    "Creates the spreadsheets in google drive"
    files_to_delete_query = drive_api.files().list(
        q=f"""
            name='{CURRENT_MONTH_NAME} {CURRENT_YEAR}' and
            mimeType='application/vnd.google-apps.spreadsheet' and
            '{GENERATED_WORKSHEETS_FOLDER_ID}' in parents and
            trashed=False
        """,
        fields="files(id)"
    ).execute()

    files_to_delete = []
    for spreadsheet in files_to_delete_query.get('files', []):
        if spreadsheet.get('id'):
            files_to_delete.append(spreadsheet['id'])

    for file_id in files_to_delete:
        drive_api.files().update(fileId=file_id, body={
            'trashed': True}).execute()

    for spreadsheet_name in spreadsheets_data:
        spreadsheet_metadata = {
            'properties': {
                'title': spreadsheet_name.capitalize()
            },
            'sheets': []
        }
        for project_name in projects_dict.values():
            spreadsheet_metadata['sheets'].append({
                'properties': {
                    'title': project_name
                }
            })

        generated_spreadsheet = (sheets_api
                                 .spreadsheets()
                                 .create(body=spreadsheet_metadata,
                                         fields='spreadsheetId')
                                 .execute())
        generated_spreadsheet_id = generated_spreadsheet.get('spreadsheetId')

        previous_parents_query = (drive_api
                                  .files()
                                  .get(fileId=generated_spreadsheet_id,
                                       fields='parents')
                                  .execute())
        previous_parents = ','.join(previous_parents_query.get('parents', ''))
        assert previous_parents
        generated_spreadsheet = (drive_api
                                 .files()
                                 .update(fileId=generated_spreadsheet_id,
                                         addParents=GENERATED_WORKSHEETS_FOLDER_ID,
                                         removeParents=previous_parents)
                                 .execute())

        spreadsheet_ids = (spreadsheet_name, generated_spreadsheet_id)
        print(f"Spreadsheet {spreadsheet_name.capitalize()} created")
    return spreadsheet_ids


def generate_rows(projects_data):
    "Converts Project data into rows for each project"
    generated_rows = {}
    for project_id, project_data in projects_data.items():
        generated_rows[project_id] = [[
            'Date',
            'Team Member',
            'Task Alotted',
            'Due Date',
            'Completed On',
            'Time Spent',
            'Status',
            'Description',
            'Project Name',
            'Project ID',
            'Reason for the delay'
        ]]
        for date, date_data in project_data.items():
            generated_rows[project_id].append([date])
            for user_name, user_data in date_data.items():
                generated_rows[project_id].append(
                    ['', user_name, *user_data[0]])
                for row in user_data[1:]:
                    generated_rows[project_id].append(['', '', *row])

    return generated_rows


def insert_records(sheets_api, spreadsheet_ids, project_data, projects_dict):
    "Insert the rows of data for each project into their sheets"
    spreadsheet_name, spreadsheet_id = spreadsheet_ids

    print(f"Uploading data into {spreadsheet_name}...")
    for project_id, sheet_data in project_data.items():
        project_name = projects_dict[project_id]

        spreadsheet_body = {
            'range': project_name,
            'values': sheet_data
        }
        (sheets_api.spreadsheets().values().append(spreadsheetId=spreadsheet_id,
                                                   range=project_name,
                                                   valueInputOption='RAW',
                                                   body=spreadsheet_body).execute())

        print('Uploaded project', project_name)


def main():
    "Loads user spreadsheets and generates project-wise spreadsheets"
    creds = utils.load_credentials()
    drive_api, sheets_api = utils.get_google_apis(creds)

    print('Loading Worksheet Folders...', end=' ')
    user_ids_dict = load_user_folders(drive_api, WORKSHEETS_FOLDER_ID)
    print('Successfully Loaded')

    print()
    print("Loading User Data...")
    user_spreadsheets_dict = load_user_spreadsheets(drive_api, user_ids_dict)

    print()
    print("Importing Spreadsheets...")
    spreadsheets_data = import_spreadsheets(sheets_api, user_spreadsheets_dict)

    print()
    project_ids = get_project_ids(spreadsheets_data)

    print()
    projects_dict, invalid_project_ids = confirm_project_names(project_ids)

    if invalid_project_ids:
        print_rows_with_invalid_ids(spreadsheets_data, invalid_project_ids)
        return

    # SAMPLE CODE TO ADD DATA TO A SPREADSHEET'S DEFAULT SHEET
    # for spreadsheet_name, spreadsheet in spreadsheets_data.items():
    #     print('Uploading spreadsheet', spreadsheet_name.capitalize())
    #     spreadsheet_id = spreadsheet['id']
    #     spreadsheet_body = {
    #         # 'range': project_name + '!A:I',
    #         'range': 'A:I',
    #         'values': spreadsheet['body']
    #     }
    #     (sheets_api.spreadsheets().values()
    #                               .append(spreadsheetId=spreadsheet_id,
    #                                       range='A:I',
    #                                       valueInputOption='RAW',
    #                                       body=spreadsheet_body)
    #                               .execute())

    print()
    print("Processing spreadsheet data...")
    projects_data, current_projects = (
        format_spreadsheets(spreadsheets_data, projects_dict)
    )
    print("Process complete.")

    print()
    print("Creating spreadsheets...")
    spreadsheet_ids = generate_spreadsheets(
        drive_api, sheets_api, spreadsheets_data, current_projects
    )

    print()
    print("Generating records...")
    generated_rows = generate_rows(projects_data)

    print()
    print("Inserting records...")
    insert_records(sheets_api, spreadsheet_ids,
                   generated_rows, current_projects)

    print()
    print("All done!")


if __name__ == '__main__':
    main()
