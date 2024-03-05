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
        {"filename": "NewHireOfficeIDs.csv", "schema": "newHireOfficeID_schema"},
        {"filename": "NewHireRequestIDs.csv", "schema": "newHireRequestID_schema"},
        {"filename": "NewHireOnboardingTaskIDs.csv", "schema": "newHireOnboardingTaskID_schema"}
    ],
    "Office": [
        {"filename": "OfficeOrganizationIDs.csv", "schema": "officeOrganizationID_schema"},
        {"filename": "OfficeAnnouncementIDs.csv", "schema": "officeAnnouncementID_schema"},
        {"filename": "OfficeApplicationIDs.csv", "schema": "officeApplicationID_schema"},
        {"filename": "OfficeCustomerIDs.csv", "schema": "officeCustomerID_schema"},
        {"filename": "OfficeNewHireIDs.csv", "schema": "officeNewHireID_schema"},
        {"filename": "OfficeVacancyIDs.csv", "schema": "officeVacancyID_schema"}
    ],
    "Organization": [
        {"filename": "OrganizationCustomerIDs.csv", "schema": "organizationCustomerID_schema"},
        {"filename": "OrganizationOfficeIDs.csv", "schema": "organizationOfficeID_schema"}
    ],
    "Request": [
        {"filename": "RequestCustomerIDs.csv", "schema": "requestCustomerID_schema"},
        {"filename": "RequestCertificateApplicationIDs.csv", "schema": "requestCertificateApplicationID_schema"},
        {"filename": "RequestNewHireIDs.csv", "schema": "requestNewHireID_schema"},
        {"filename": "RequestOnboardingTaskIDs.csv", "schema": "requestOnboardingTaskID_schema"},
        {"filename": "RequestReviewIDs.csv", "schema": "requestReviewID_schema"},
        {"filename": "RequestStaffingTaskIDs.csv", "schema": "requestStaffingTaskID_schema"},
        {"filename": "RequestVacancyIDs.csv", "schema": "requestVacancyID_schema"}
    ],
    "TimeToHire": [
        {"filename": "TimeToHireAnnouncementIDs.csv", "schema": "timeToHireAnnouncementID_schema"},
        {"filename": "TimeToHireCustomerIDs.csv", "schema": "timeToHireCustomerID_schema"},
        {"filename": "TimeToHireOfficeIDs.csv", "schema": "timeToHireOfficeID_schema"},
        {"filename": "TimeToHireOrganizationIDs.csv", "schema": "timeToHireOrganizationID_schema"},
        {"filename": "TimeToHireRequestIDs.csv", "schema": "timeToHireRequestID_schema"},
        {"filename": "TimeToHireVacancyIDs.csv", "schema": "timeToHireVacancyID_schema"},
        {"filename": "TimeToHireNewHireIDs.csv", "schema": "timeToHireNewHireID_schema"}
    ],
    "Vacancy": [
        {"filename": "VacancyAnnouncementIDs.csv", "schema": "vacancyAnnouncementID_schema"},
        {"filename": "VacancyApplicationIDs.csv", "schema": "vacancyApplicationID_schema"},
        {"filename": "VacancyAssessmentIDs.csv", "schema": "vacancyAssessmentID_schema"},
        {"filename": "VacancyCertificateIDs.csv", "schema": "vacancyCertificateID_schema"},
        {"filename": "VacancyCustomerIDs.csv", "schema": "vacancyCustomerID_schema"},
        {"filename": "VacancyOfficeIDs.csv", "schema": "vacancyOfficeID_schema"},
        {"filename": "VacancyRequestIDs.csv", "schema": "vacancyRequestID_schema"},
        {"filename": "VacancyReviewIDs.csv", "schema": "vacancyReviewID_schema"},
        {"filename": "VacancyStaffingTaskIDs.csv", "schema": "vacancyStaffingTaskID_schema"}
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
