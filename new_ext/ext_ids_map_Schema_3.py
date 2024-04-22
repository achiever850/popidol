certificateApplicationApplicationIDs_schema = StructType([
        StructField("TenantID", IntegerType(), True),
        StructField("cA_Ranking_ListID", LongType(), True),
        StructField("cA_ApplicationID", LongType(), True),
        StructField("applicationID", LongType(), True)
    ])
    certificateApplicationRankingListIDs_schema = StructType([
        StructField("TenantID", IntegerType(), True),
        StructField("cA_Ranking_ListID", LongType(), True),
        StructField("cA_ApplicationID", LongType(), True),
        StructField("RankingListID", LongType(), True)
    ])
    certificateApplicationNewHireIDs_schema = StructType([
        StructField("TenantID", IntegerType(), True),
        StructField("cA_Ranking_ListID", LongType(), True),
        StructField("cA_ApplicationID", LongType(), True),
        StructField("NewHireID", LongType(), True)
    ])
    certificateApplicationRequestIDs_schema = StructType([
        StructField("TenantID", IntegerType(), True),
        StructField("cA_Ranking_ListID", LongType(), True),
        StructField("cA_ApplicationID", LongType(), True),
        StructField("RequestID", LongType(), True)
    ])
    certificateVacancyIDs_schema = StructType([
        StructField("VacancyID", IntegerType(), True),
        StructField("ApplicationID", LongType(), True),
        StructField("ReviewID", LongType(), True)
    ])
    certificateCertificateApplicationID_schema = StructType([
        StructField("VacancyID", IntegerType(), True),
        StructField("CertificateApplicationID", LongType(), True),
        StructField("ReviewID", LongType(), True)
    ])
    certificateReviewIDs_schema = StructType([
        StructField("VacancyID", IntegerType(), True),
        StructField("Certificate ApplicationID", LongType(), True),
        StructField("ReviewID", LongType(), True)
    ])
    reviewAssessmentIDs_schema = StructType([
        StructField("TenantID", IntegerType(), True),
        StructField("ReviewID", LongType(), True),
        StructField("AssessmentID", LongType(), True)
    ])
    reviewCertificateIDs_schema = StructType([
        StructField("TenantID", IntegerType(), True),
        StructField("ReviewID", LongType(), True),
        StructField("RankingListID", LongType(), True)
    ])
    reviewRequestIDs_schema = StructType([
        StructField("TenantID", IntegerType(), True),
        StructField("ReviewID", LongType(), True),
        StructField("RequestID", LongType(), True)
    ])
    reviewVacancyIDs_schema = StructType([
        StructField("TenantID", IntegerType(), True),
        StructField("ReviewID", LongType(), True),
        StructField("VacancyID", LongType(), True)
    ])
    StaffingTask_schema = StructType([
        StructField("TenantID", IntegerType(), True),
        StructField("TaskID", LongType(), True),
        StructField("RequestID", LongType(), True)
    ])
    StaffingTask_schema = StructType([
        StructField("TenantID", IntegerType(), True),
        StructField("TaskID", LongType(), True),
        StructField("VacancyID", LongType(), True)
    ])
    applicationOfficeIDs_schema = StructType([
        StructField("TenantID", IntegerType(), True),
        StructField("ApplicationID", LongType(), True),
        StructField("OfficeID", LongType(), True)
    ])
    applicationVacancyIDs_schema = StructType([
        StructField("TenantID", IntegerType(), True),
        StructField("ApplicationID", LongType(), True),
        StructField("VacancyID", LongType(), True)
    ])
    applicationCertificateApplicationIDs_schema = StructType([
        StructField("TenantID", IntegerType(), True),
        StructField("ApplicationID", LongType(), True),
        StructField("CertificateApplicationID", LongType(), True)
    ])
    onboardingTasksNewHireID_schema = StructType([
        StructField("TenantID", IntegerType(), True),
        StructField("OnboardingTaskID", LongType(), True),
        StructField("NewHireID", LongType(), True)
    ])
    onboardingTasksRequestID_schema = StructType([
        StructField("TenantID", IntegerType(), True),
        StructField("OnboardingTaskID", LongType(), True),
        StructField("RequestID", LongType(), True)
    ])
    
