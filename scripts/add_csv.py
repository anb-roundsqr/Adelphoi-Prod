# python manage.py runscript add_csv
# --script-args location_dir/saturday_7_0.xlsx

from datetime import date
import pandas as pd
from FirstMatch.models import ModelTests


def run(*args):
    if args[0].endswith(".xlsx"):
        df = pd.read_excel(args[0])
    else:
        df = pd.read_csv(args[0])

    def calculateAge(birthDate):
        today = date.today()
        age = today.year - birthDate.year - (
                (today.month, today.day) < (birthDate.month, birthDate.day))
        return age

    df['Age'] = df['DoB'].apply(calculateAge)
    df_obj = df.select_dtypes(include=["object"])
    for col in df_obj.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    df_1 = df[df['Gender'] == 1]
    values = {
        'Family support': 1,
        'Level of aggression': 2,
        'Fire setting': 0,
        'Client self-harm': 0,
        'Abuse, or neglect': 1,
        'CANS_LifeFunctioning': 13,
        'CANS_YouthStrengths': 14,
        'CANS_CareGiverStrengths': 10,
        'CANS_Culture': 0,
        'CANS_YouthBehavior': 9,
        'CANS_YouthRisk': 4,
        'CANS_Trauma_Exp': 5,
        'FAST_FamilyTogetherScore': 8,
        'FAST_CaregiverAdvocacyScore': 7,
        'YLS_PriorCurrentOffenses_Score': 1,
        'YLS_FamCircumstances_Score': 4,
        'YLS_Edu_Employ_Score': 3,
        'YLS_Peer_Score': 3,
        'YLS_Subab_Score': 2,
        'YLS_Leisure_Score': 2,
        'YLS_Personality_Score': 4,
        'YLS_Attitude_Score': 10,
        'Screening tool for Trauma--Total score': 15
    }
    df_1 = df_1.fillna(value=values)
    df_2 = df[df['Gender'] == 2]
    value = {
        'Family support': 1,
        'Level of aggression': 2,
        'Fire setting': 0,
        'Client self-harm': 0,
        'Abuse, or neglect': 1,
        'CANS_LifeFunctioning': 11,
        'CANS_YouthStrengths': 13,
        'CANS_CareGiverStrengths': 7,
        'CANS_Culture': 0,
        'CANS_YouthBehavior': 8,
        'CANS_YouthRisk': 4,
        'CANS_Trauma_Exp': 4,
        'FAST_FamilyTogetherScore': 7,
        'FAST_CaregiverAdvocacyScore': 6,
        'YLS_PriorCurrentOffenses_Score': 1,
        'YLS_FamCircumstances_Score': 3,
        'YLS_Edu_Employ_Score': 2,
        'YLS_Peer_Score': 2,
        'YLS_Subab_Score': 1,
        'YLS_Leisure_Score': 2,
        'YLS_Personality_Score': 3,
        'YLS_Attitude_Score': 1,
        'Screening tool for Trauma--Total score': 15
    }
    df_2 = df_2.fillna(value=value)
    df = pd.concat([df_1, df_2])
    df.fillna(0, inplace=True)

    numeric_cols = [
        'PrimaryRacecode', 'SecondaryRaceCode', 'PrimaryLanguage',
        'CYF_code', 'EnrollmentStatus', 'Level_of_Care', 'RefSourceCode',
        'ClientDischarge', 'ReturntoCare_c',
        'Number of prior treatment terminations'
        ' (excluding shelter or detention)',
        'Length of time since living at home',
        'Termination directly to AV',
        'Death Caregiver', 'Death Silblings', 'Alcohol Use',
        'English as the second language', 'Incarcerated caregivers',
        'Incarcerated siblings', 'Number of prior AWOLS', 'Animal cruelty',
        'Hist of prior program SAO', 'Number of prior hospitalizations',
        'Compliant with medication', 'Significant mental health symptoms',
        'Severe mental health symptoms', 'Autism Diagnosis',
        'Borderline Personality', 'Psychosis', 'Reactive Attachment Disorder',
        'Schizophrenia', 'Family support', 'Level of aggression',
        'Fire setting', 'Client self-harm', 'Abuse, or neglect',
        'CANS_LifeFunctioning', 'CANS_YouthStrengths',
        'CANS_CareGiverStrengths', 'CANS_Culture', 'CANS_YouthBehavior',
        'CANS_YouthRisk', 'CANS_Trauma_Exp', 'FAST_FamilyTogetherScore',
        'FAST_CaregiverAdvocacyScore', 'YLS_PriorCurrentOffenses_Score',
        'YLS_FamCircumstances_Score', 'YLS_Edu_Employ_Score',
        'YLS_Peer_Score', 'YLS_Subab_Score', 'YLS_Leisure_Score',
        'YLS_Personality_Score', 'YLS_Attitude_Score',
        'Screening tool for Trauma--Total score'
    ]
    for col in numeric_cols:
        df[col] = df[col].fillna(0).astype(int)

    # df_flt11 = df.select_dtypes(include=["float"])
    df[['Type of drugs listed',
        'ClientDx', 'Level of care of previous termination']] = \
        df[['Type of drugs listed', 'ClientDx',
            'Level of care of previous termination']].astype(str)

    for i in df.to_dict('records'):
        ModelTests(
            episode_start=i['EpisodeStart'],
            episode_number=i['EpisodeNumber'],
            client_code=i['ClientCode'],
            dob=i['DoB'],
            gender=i['Gender'],
            primary_language=i['PrimaryLanguage'],
            RefSourceCode=i['RefSourceCode'],
            ls_type=i['LS_Type'],
            CYF_code=i['CYF_code'],
            number_of_prior_placements=i[
                'Number of prior placements'
                ' \n(excluding shelter and detention)'
            ],
            number_of_foster_care_placements=i[
                'Number of foster care placements'
            ],
            number_of_prior_AWOLS=i['Number of prior AWOLS'],
            number_of_prior_treatment_terminations=i[
                'Number of prior treatment terminations'
                ' (excluding shelter or detention)'
            ],
            termination_directly_to_AV=i['Termination directly to AV'],
            length_of_time_since_living_at_home=i[
                'Length of time since living at home'
            ],
            hist_of_prior_program_SAO=i['Hist of prior program SAO'],
            autism_Diagnosis=i['Autism Diagnosis'],
            borderline_Personality=i['Borderline Personality'],
            reactive_Attachment_Disorder=i[
                'Reactive Attachment Disorder'
            ],
            animal_cruelty=i['Animal cruelty'],
            schizophrenia=i['Schizophrenia'],
            psychosis=i['Psychosis'], borderline_IQ=i[
                'Borderline IQ (below 70)'
            ],
            significant_mental_health_symptoms=i[
                'Significant mental health symptoms'
            ],
            prior_hospitalizations=i[
                'Number of prior hospitalizations'
            ],
            severe_mental_health_symptoms=i[
                'Severe mental health symptoms'
            ],
            compliant_with_meds=i['Compliant with medication'],
            incarcerated_caregivers=i['Incarcerated caregivers'],
            death_Caregiver=i['Death Caregiver'],
            incarcerated_siblings=i['Incarcerated siblings'],
            death_Silblings=i['Death Silblings'],
            alcohol_Use=i['Alcohol Use'],
            drug_Use=i['Drug Use'],
            abuse_neglect=i['Abuse, or neglect'],
            yls_FamCircumstances_Score=i[
                'YLS_FamCircumstances_Score'
            ],
            yls_Edu_Employ_Score=i['YLS_Edu_Employ_Score'],
            yls_Peer_Score=i['YLS_Peer_Score'],
            yls_Subab_Score=i['YLS_Subab_Score'],
            yls_Leisure_Score=i['YLS_Leisure_Score'],
            yls_Personality_Score=i['YLS_Personality_Score'],
            yls_Attitude_Score=i['YLS_Attitude_Score'],
            yls_PriorCurrentOffenses_Score=i[
                'YLS_PriorCurrentOffenses_Score'
            ],
            family_support=i['Family support'],
            fire_setting=i['Fire setting'],
            level_of_aggression=i['Level of aggression'],
            client_self_harm=i['Client self-harm'],
            Screening_tool_Trauma=i[
                'Screening tool for Trauma--Total score'
            ],
            cans_LifeFunctioning=i['CANS_LifeFunctioning'],
            cans_YouthStrengths=i['CANS_YouthStrengths'],
            cans_CareGiverStrengths=i['CANS_CareGiverStrengths'],
            cans_Culture=i['CANS_Culture'],
            cans_YouthBehavior=i['CANS_YouthBehavior'],
            cans_YouthRisk=i['CANS_YouthRisk'],
            cans_Trauma_Exp=i['CANS_Trauma_Exp'],
            ageAtEpisodeStart=i['AgeAtEpisodeStart'],
            enrollStart_date=i['EnrollStart'],
            ageAtEnrollStart=i['AgeAtEnrollStart'],
            type_of_drugs=i['Type of drugs listed'],
            FAST_FamilyTogetherScore=i['FAST_FamilyTogetherScore'],
            FAST_CaregiverAdvocacyScore=i[
                'FAST_CaregiverAdvocacyScore'
            ],
            Program_Completion=i['ProgramCompletion'],
            Returned_to_Care=i['ReturntoCare_c'],
            level_of_care=i['Level_of_Care'],
            program=i['Program'],
            facility_type=i['FacilityType']
        ).save()
