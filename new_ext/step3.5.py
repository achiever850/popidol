import extids_map_schema as extids_schema

table_dict = {
    1:"Announcement",
    2:"Application",
    3:"Assessment",
    4:"CertificateApplication",
    5:"Certificate",
    6:"Customer",
    7:"NewHire",
    8:"NewHireAppointingAuthority",
    9:"Office",
    10:"OnboardingTask",
    11:"Organization",
    12:"RequestAppointingAuthority",
    13:"Request",
    14:"Review",
    15:"StaffingTask",
    16:"TimeToHire",
    17:"VacancyAppointingAuthority",
    18:"VacancyFlag",
    19:"Vacancy"}

process_tables = [6,7,9,13,16,19]

ext_schema_data = {
    "Customer": [
        {"filename": "customerAnnouncementIDs.csv", "schema": "customerAnnouncementID_schema"},
        {"filename": "customerOfficeIDs.csv", "schema": "customerOfficeID_schema"},
        {"filename": "customerOrganizationIDs.csv", "schema": "customerOrganizationID_schema"},
        {"filename": "customerRequestIDs.csv", "schema": "customerRequestID_schema"},
        {"filename": "customerVacancyIDs.csv", "schema": "customerVacancyID_schema"}
    ],
    "NewHire": [
        {"filename": "OfficeIDs.csv", "schema": "newHireOfficeID_schema"},
        {"filename": "RequestIDs.csv", "schema": "newHireRequestID_schema"},
        {"filename": "OnboardingTaskIDs.csv", "schema": "newHireOnboardingTaskID_schema"}
    ],
    "Office": [
        {"filename": "OrganizationIDs.csv", "schema": "officeOrganizationID_schema"},
        {"filename": "AnnouncementIDs.csv", "schema": "officeAnnouncementID_schema"},
        {"filename": "ApplicationIDs.csv", "schema": "officeApplicationID_schema"},
        {"filename": "CustomerIDs.csv", "schema": "officeCustomerID_schema"},
        {"filename": "NewHireIDs.csv", "schema": "officeNewHireID_schema"},
        {"filename": "VacancyIDs.csv", "schema": "officeVacancyID_schema"}
    ],
    "Organization": [
        {"filename": "CustomerIDs.csv", "schema": "organizationCustomerID_schema"},
        {"filename": "OfficeIDs.csv", "schema": "organizationOfficeID_schema"}
    ],
    "Request": [
        {"filename": "CustomerIDs.csv", "schema": "requestCustomerID_schema"},
        {"filename": "CertificateApplicationIDs.csv", "schema": "requestCertificateApplicationID_schema"},
        {"filename": "NewHireIDs.csv", "schema": "requestNewHireID_schema"},
        {"filename": "OnboardingTaskIDs.csv", "schema": "requestOnboardingTaskID_schema"},
        {"filename": "ReviewIDs.csv", "schema": "requestReviewID_schema"},
        {"filename": "StaffingTaskIDs.csv", "schema": "requestStaffingTaskID_schema"},
        {"filename": "VacancyIDs.csv", "schema": "requestVacancyID_schema"}
    ],
    "TimeToHire": [
        {"filename": "AnnouncementIDs.csv", "schema": "timeToHireAnnouncementID_schema"},
        {"filename": "CustomerIDs.csv", "schema": "timeToHireCustomerID_schema"},
        {"filename": "OfficeIDs.csv", "schema": "timeToHireOfficeID_schema"},
        {"filename": "OrganizationIDs.csv", "schema": "timeToHireOrganizationID_schema"},
        {"filename": "RequestIDs.csv", "schema": "timeToHireRequestID_schema"},
        {"filename": "VacancyIDs.csv", "schema": "timeToHireVacancyID_schema"},
        {"filename": "NewHireIDs.csv", "schema": "timeToHireNewHireID_schema"}
    ],
    "Vacancy": [
        {"filename": "AnnouncementIDs.csv", "schema": "vacancyAnnouncementID_schema"},
        {"filename": "ApplicationIDs.csv", "schema": "vacancyApplicationID_schema"},
        {"filename": "AssessmentIDs.csv", "schema": "vacancyAssessmentID_schema"},
        {"filename": "CertificateIDs.csv", "schema": "vacancyCertificateID_schema"},
        {"filename": "CustomerIDs.csv", "schema": "vacancyCustomerID_schema"},
        {"filename": "OfficeIDs.csv", "schema": "vacancyOfficeID_schema"},
        {"filename": "RequestIDs.csv", "schema": "vacancyRequestID_schema"},
        {"filename": "ReviewIDs.csv", "schema": "vacancyReviewID_schema"},
        {"filename": "StaffingTaskIDs.csv", "schema": "vacancyStaffingTaskID_schema"}
    ]
}

def get_file_path(filename):
    for file in available_csv_files_li:
        if(filename in file):
            return file
    return None

for i in process_tables:
    table_name = table_dict[i]
    extid_schemas_li = ext_schema_data[table_name]
    for sch_key in extid_schemas_li:
        filename = sch_key['filename']
        act_file = get_file_path(filename)
        if(act_file):
            struct_schema = getattr(extids_schema, sch_key['schema'])
            execute_csv(act_file,struct_schema)
        else:
            print(f"Missing the file {filename} for {table_name} ")
