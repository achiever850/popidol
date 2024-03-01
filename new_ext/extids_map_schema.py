from pyspark.sql.types import StructType, StructField, IntegerType, LongType

customerAnnouncementID_schema = StructType([
    StructField("Tenant_ID", IntegerType(), True),
    StructField("Customer_ID", LongType(), True),
    StructField("Announcement_ID", LongType(), True)
])

customerOfficeID_schema = StructType([
    StructField("Tenant_ID", IntegerType(), True),
    StructField("Customer_ID", LongType(), True),
    StructField("Office_ID", LongType(), True)
])

customerOrganizationID_schema = StructType([
    StructField("Tenant_ID", IntegerType(), True),
    StructField("Customer_ID", LongType(), True),
    StructField("Organization_ID", LongType(), True)
])

customerRequestID_schema = StructType([
    StructField("Tenant_ID", IntegerType(), True),
    StructField("Customer_ID", LongType(), True),
    StructField("Request_ID", LongType(), True)
])

customerVacancyID_schema = StructType([
    StructField("Tenant_ID", IntegerType(), True),
    StructField("Customer_ID", LongType(), True),
    StructField("Vacancy_ID", LongType(), True)
])

newHireOfficeID_schema = StructType([
    StructField("Tenant_ID", IntegerType(), True),
    StructField("NewHire_ID", LongType(), True),
    StructField("Office_ID", LongType(), True)
])

newHireRequestID_schema = StructType([
    StructField("Tenant_ID", IntegerType(), True),
    StructField("NewHire_ID", LongType(), True),
    StructField("Request_ID", LongType(), True)
])

newHireOnboardingTaskID_schema = StructType([
    StructField("Tenant_ID", IntegerType(), True),
    StructField("NewHire_ID", LongType(), True),
    StructField("Task_ID", LongType(), True)
])


officeOrganizationID_schema = StructType([
    StructField("Tenant_ID", IntegerType(), True),
    StructField("Office_ID", LongType(), True),
    StructField("Organization_ID", LongType(), True)
])

officeAnnouncementID_schema = StructType([
    StructField("Tenant_ID", IntegerType(), True),
    StructField("Office_ID", LongType(), True),
    StructField("Announcement_ID", LongType(), True)
])

officeApplicationID_schema = StructType([
    StructField("Tenant_ID", IntegerType(), True),
    StructField("Office_ID", LongType(), True),
    StructField("Application_ID", LongType(), True)
])

officeCustomerID_schema = StructType([
    StructField("Tenant_ID", IntegerType(), True),
    StructField("Office_ID", LongType(), True),
    StructField("Customer_ID", LongType(), True)
])

officeNewHireID_schema = StructType([
    StructField("Tenant_ID", IntegerType(), True),
    StructField("Office_ID", LongType(), True),
    StructField("New_Hire_ID", LongType(), True)
])

officeVacancyID_schema = StructType([
    StructField("Tenant_ID", IntegerType(), True),
    StructField("Office_ID", LongType(), True),
    StructField("Vacancy_ID", LongType(), True)
])

requestCustomerID_schema = StructType([
    StructField("Tenant_ID", IntegerType(), True),
    StructField("Request_ID", LongType(), True),
    StructField("Customer_ID", LongType(), True)
])

requestCertificateApplicationID_schema = StructType([
    StructField("Tenant_ID", IntegerType(), True),
    StructField("Request_ID", LongType(), True),
    StructField("Certificate_Application_ID", LongType(), True)
])

requestNewHireID_schema = StructType([
    StructField("Tenant_ID", IntegerType(), True),
    StructField("Request_ID", LongType(), True),
    StructField("New_Hire_ID", LongType(), True)
])

requestOnboardingTaskID_schema = StructType([
    StructField("Tenant_ID", IntegerType(), True),
    StructField("Request_ID", LongType(), True),
    StructField("Onboarding_Task_ID", LongType(), True)
])

requestReviewID_schema = StructType([
    StructField("Tenant_ID", IntegerType(), True),
    StructField("Request_ID", LongType(), True),
    StructField("Review_ID", LongType(), True)
])

requestStaffingTaskID_schema = StructType([
    StructField("Tenant_ID", IntegerType(), True),
    StructField("Request_ID", LongType(), True),
    StructField("Staffing_Task_ID", LongType(), True)
])

requestVacancyID_schema = StructType([
    StructField("Tenant_ID", IntegerType(), True),
    StructField("Request_ID", LongType(), True),
    StructField("Vacancy_ID", LongType(), True)
])

timeToHireAnnouncementID_schema = StructType([
    StructField("Tenant_ID", IntegerType(), True),
    StructField("TimeToHire_ID", LongType(), True),
    StructField("Announcement_ID", LongType(), True)
])

timeToHireCustomerID_schema = StructType([
    StructField("Tenant_ID", IntegerType(), True),
    StructField("TimeToHire_ID", LongType(), True),
    StructField("Customer_ID", LongType(), True)
])

timeToHireOfficeID_schema = StructType([
    StructField("Tenant_ID", IntegerType(), True),
    StructField("TimeToHire_ID", LongType(), True),
    StructField("Office_ID", LongType(), True)
])

timeToHireOrganizationID_schema = StructType([
    StructField("Tenant_ID", IntegerType(), True),
    StructField("TimeToHire_ID", LongType(), True),
    StructField("Org_ID", LongType(), True)
])

timeToHireRequestID_schema = StructType([
    StructField("Tenant_ID", IntegerType(), True),
    StructField("TimeToHire_ID", LongType(), True),
    StructField("Request_ID", LongType(), True)
])

timeToHireVacancyID_schema = StructType([
    StructField("Tenant_ID", IntegerType(), True),
    StructField("TimeToHire_ID", LongType(), True),
    StructField("Vacancy_ID", LongType(), True)
])

timeToHireNewHireID_schema = StructType([
    StructField("Tenant_ID", IntegerType(), True),
    StructField("TimeToHire_ID", LongType(), True),
    StructField("NewHire_ID", LongType(), True)
])

vacancyAnnouncementID_schema = StructType([
    StructField("Tenant_ID", IntegerType(), True),
    StructField("Vacancy_ID", LongType(), True),
    StructField("Announcement_ID", LongType(), True)
])

vacancyApplicationID_schema = StructType([
    StructField("Tenant_ID", IntegerType(), True),
    StructField("Vacancy_ID", LongType(), True),
    StructField("Application_ID", LongType(), True)
])

vacancyAssessmentID_schema = StructType([
    StructField("Tenant_ID", IntegerType(), True),
    StructField("Vacancy_ID", LongType(), True),
    StructField("Assessment_ID", LongType(), True)
])

vacancyCertificateID_schema = StructType([
    StructField("Tenant_ID", IntegerType(), True),
    StructField("Vacancy_ID", LongType(), True),
    StructField("Certificate_ID", LongType(), True)
])

vacancyCustomerID_schema = StructType([
    StructField("Tenant_ID", IntegerType(), True),
    StructField("Vacancy_ID", LongType(), True),
    StructField("Customer_ID", LongType(), True)
])

vacancyOfficeID_schema = StructType([
    StructField("Tenant_ID", IntegerType(), True),
    StructField("Vacancy_ID", LongType(), True),
    StructField("Office_ID", LongType(), True)
])

vacancyRequestID_schema = StructType([
    StructField("Tenant_ID", IntegerType(), True),
    StructField("Vacancy_ID", LongType(), True),
    StructField("Request_ID", LongType(), True)
])

vacancyReviewID_schema = StructType([
    StructField("Tenant_ID", IntegerType(), True),
    StructField("Vacancy_ID", LongType(), True),
    StructField("Review_ID", LongType(), True)
])

vacancyStaffingTaskID_schema = StructType([
    StructField("Tenant_ID", IntegerType(), True),
    StructField("Vacancy_ID", LongType(), True),
    StructField("Task_ID", LongType(), True)
])

requestCustomerID_schema = StructType([
    StructField("Tenant_ID", IntegerType(), True),
    StructField("Request_ID", LongType(), True),
    StructField("Customer_ID", LongType(), True)
])

requestCertificateApplicationID_schema = StructType([
    StructField("Tenant_ID", IntegerType(), True),
    StructField("Request_ID", LongType(), True),
    StructField("Certificate_Application_ID", LongType(), True)
])

requestNewHireID_schema = StructType([
    StructField("Tenant_ID", IntegerType(), True),
    StructField("Request_ID", LongType(), True),
    StructField("New_Hire_ID", LongType(), True)
])

requestOnboardingTaskID_schema = StructType([
    StructField("Tenant_ID", IntegerType(), True),
    StructField("Request_ID", LongType(), True),
    StructField("Onboarding_Task_ID", LongType(), True)
])

requestReviewID_schema = StructType([
    StructField("Tenant_ID", IntegerType(), True),
    StructField("Request_ID", LongType(), True),
    StructField("Review_ID", LongType(), True)
])

requestStaffingTaskID_schema = StructType([
    StructField("Tenant_ID", IntegerType(), True),
    StructField("Request_ID", LongType(), True),
    StructField("Staffing_Task_ID", LongType(), True)
])

requestVacancyID_schema = StructType([
    StructField("Tenant_ID", IntegerType(), True),
    StructField("Request_ID", LongType(), True),
    StructField("Vacancy_ID", LongType(), True)
])
