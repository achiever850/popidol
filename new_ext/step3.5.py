
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
    "Customer": ["customerAnnouncementID_schema", "customerOfficeID_schema", "customerOrganizationID_schema",   "customerRequestID_schema", "customerVacancyID_schema"],
    "NewHire": ["newHireOfficeID_schema", "newHireRequestID_schema", "newHireOnboardingTaskID_schema"],
    "Office": ["officeOrganizationID_schema", "officeAnnouncementID_schema", "officeApplicationID_schema", "officeCustomerID_schema", "officeNewHireID_schema", "officeVacancyID_schema"],
    "Organization": ["organizationCustomerID_schema", "organizationOfficeID_schema"],  
    "Request": ["requestCustomerID_schema", "requestCertificateApplicationID_schema", "requestNewHireID_schema", "requestOnboardingTaskID_schema", "requestReviewID_schema", "requestStaffingTaskID_schema", "requestVacancyID_schema"],
    "TimeToHire": ["timeToHireAnnouncementID_schema", "timeToHireCustomerID_schema", "timeToHireOfficeID_schema", "timeToHireOrganizationID_schema", "timeToHireRequestID_schema", "timeToHireVacancyID_schema", "timeToHireNewHireID_schema"],
    "Vacancy": ["vacancyAnnouncementID_schema", "vacancyApplicationID_schema", "vacancyAssessmentID_schema", "vacancyCertificateID_schema", "vacancyCustomerID_schema", "vacancyOfficeID_schema", "vacancyRequestID_schema", "vacancyReviewID_schema", "vacancyStaffingTaskID_schema"]
}


for i in process_tables:
    table_name = table_dict[i]
    extid_schemas_li = ext_schema_data[table_name]
    for sch in extid_schemas_li:
        struct_schema = getattr(extids_schema, sch)
        print(struct_schema)
