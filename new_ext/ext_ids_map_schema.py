from pyspark.sql.types import StructType, StructField, IntegerType, LongType

announcementCustomerID_schema = StructType([
    StructField("TenantID", IntegerType(), True),
    StructField("AnnouncementID", LongType(), True),
    StructField("CustomerID", LongType(), True)
])
announcementOfficeID_schema = StructType([
    StructField("TenantID", IntegerType(), True),
    StructField("AnnouncementID", LongType(), True),
    StructField("OfficeID", LongType(), True)
])
announcementVacancyID_schema = StructType([
    StructField("TenantID", IntegerType(), True),
    StructField("AnnouncementID", LongType(), True),
    StructField("VacancyID", LongType(), True)
])
assessmentReviewID_schema = StructType([
    StructField("TenantID", IntegerType(), True),
    StructField("AssessmentID", LongType(), True),
    StructField("ReviewID", LongType(), True)
])
assessmentVacancyID_schema = StructType([
    StructField("TenantID", IntegerType(), True),
    StructField("AssessmentID", LongType(), True),
    StructField("VacancyID", LongType(), True)
])
certificateVacancyID_schema = StructType([
    StructField("VacancyID", IntegerType(), True),
    StructField("ApplicationID", LongType(), True),
    StructField("ReviewID", LongType(), True)
])
certificateCertificateApplicationID_schema = StructType([
    StructField("VacancyID", IntegerType(), True),
    StructField("CertificateApplicationID", LongType(), True),
    StructField("ReviewID", LongType(), True)
])
certificateReviewID_schema = StructType([
    StructField("VacancyID", IntegerType(), True),
    StructField("CertificateApplicationID", LongType(), True),
    StructField("ReviewID", LongType(), True)
])
vacancyAnnouncementID_schema = StructType([
    StructField("TenantID", IntegerType(), True),
    StructField("VacancyID", LongType(), True),
    StructField("AnnouncementID", LongType(), True)
])
vacancyApplicationID_schema = StructType([
    StructField("TenantID", IntegerType(), True),
    StructField("VacancyID", LongType(), True),
    StructField("ApplicationID", LongType(), True)
])
vacancyAssessmentID_schema = StructType([
    StructField("TenantID", IntegerType(), True),
    StructField("VacancyID", LongType(), True),
    StructField("AssessmentID", LongType(), True)
])
vacancyCertificateID_schema = StructType([
    StructField("TenantID", IntegerType(), True),
    StructField("VacancyID", LongType(), True),
    StructField("CertificateID", LongType(), True)
])
vacancyCustomerID_schema = StructType([
    StructField("TenantID", IntegerType(), True),
    StructField("VacancyID", LongType(), True),
    StructField("CustomerID", LongType(), True)
])
vacancyOfficeID_schema = StructType([
    StructField("TenantID", IntegerType(), True),
    StructField("VacancyID", LongType(), True),
    StructField("OfficeID", LongType(), True)
])
vacancyRequestID_schema = StructType([
    StructField("TenantID", IntegerType(), True),
    StructField("VacancyID", LongType(), True),
    StructField("RequestID", LongType(), True)
])
vacancyReviewID_schema = StructType([
    StructField("TenantID", IntegerType(), True),
    StructField("VacancyID", LongType(), True),
    StructField("ReviewID", LongType(), True)
])
vacancyStaffingTaskID_schema = StructType([
    StructField("TenantID", IntegerType(), True),
    StructField("VacancyID", LongType(), True),
    StructField("TaskID", LongType(), True)
])
reviewAssessmentID_schema = StructType([
    StructField("TenantID", IntegerType(), True),
    StructField("ReviewID", LongType(), True),
    StructField("AssessmentID", LongType(), True)
])
reviewCertificateID_schema = StructType([
    StructField("TenantID", IntegerType(), True),
    StructField("ReviewID", LongType(), True),
    StructField("Ranking ListID", LongType(), True)
])
reviewRequestID_schema = StructType([
    StructField("TenantID", IntegerType(), True),
    StructField("ReviewID", LongType(), True),
    StructField("RequestID", LongType(), True)
])
reviewVacancyID_schema = StructType([
    StructField("TenantID", IntegerType(), True),
    StructField("ReviewID", LongType(), True),
    StructField("VacancyID", LongType(), True)
])
staffingtaskRequestID_schema = StructType([
    StructField("TenantID", IntegerType(), True),
    StructField("TaskID", LongType(), True),
    StructField("RequestID", LongType(), True)
])
staffingtaskVacancyID_schema = StructType([
    StructField("TenantID", IntegerType(), True),
    StructField("TaskID", LongType(), True),
    StructField("VacancyID", LongType(), True)
])
